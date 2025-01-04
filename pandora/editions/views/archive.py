import urllib.parse
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime, time
from django.core.exceptions import ValidationError
from django.core.files import File as DjangoFile
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView

from pandora.editions.forms.archive import ArchiveUploadForm
from pandora.editions.mixins import CommitteeMemberAccessMixin
from pandora.editions.models import Edition, Day, EditionSetting, ArchiveScore, EditionMediaItem
from pandora.pregames.models import PregamePuzzleCode, Pregame
from pandora.puzzles.models import Puzzle, PuzzleCode, PuzzleFile
from pandora.teams.models import Team

START_DATE_BY_YEAR = {
    2023: date(2023, 5, 8),
    2022: date(2022, 5, 9),
    2021: date(2021, 5, 30),
    2019: date(2019, 5, 20),
    2018: date(2018, 5, 14),
    2017: date(2017, 5, 15),
    2016: date(2016, 5, 9),
    2015: date(2015, 5, 18),
    2014: date(2014, 5, 12),
    2013: date(2013, 5, 13),
    2012: date(2012, 5, 6),
    2011: date(2011, 4, 25),
    2010: date(2010, 5, 24),
    2009: date(2009, 5, 10),
    2007: date(2007, 2, 25)
}


class ArchiveUploadView(CommitteeMemberAccessMixin, FormView):
    form_class = ArchiveUploadForm
    template_name = 'editions/archive_upload.html'
    success_url = reverse_lazy('archive_upload')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    @transaction.atomic
    def form_valid(self, form):
        with (ZipFile(form.cleaned_data.get('file'), 'r') as zip_file):
            info_list = zip_file.infolist()

            def find_info(filename: str):
                for info_entry in info_list:
                    if info_entry.filename == filename:
                        return info_entry
                raise ValidationError(f'Could not find file "{filename}".')

            for info in info_list:
                if '/' in info.filename or not info.filename.endswith('.html'):
                    continue

                with zip_file.open(info, 'r') as html_file:
                    soup = BeautifulSoup(html_file.read(), 'html.parser')

                    for edition_element in soup.css.select('.container > section > .card > .card-body > .card'):
                        edition_title = edition_element.css.select_one('.card-header a').get_text().strip()
                        edition_year = int(edition_title[0:4])
                        edition_name = edition_title[5:]

                        score_rows = []
                        sections = []

                        if edition_element.css.select_one('.card-body > section:nth-child(1) > table'):
                            column_names = [td_element.get_text().strip() for td_element in
                                            edition_element.css.select('.card-body > section:nth-child(1) > table > thead > tr > td')]

                            for row_element in edition_element.css.select('.card-body > section:nth-child(1) > table > tbody > tr'):
                                score_row = {}

                                for index, column_element in enumerate(row_element.css.select('td')):
                                    score_row[column_names[index]] = column_element.get_text().strip()

                                score_rows.append(score_row)

                        for section_element in edition_element.css.select('.card-body > section'):
                            if section_element.css.select_one('table'):
                                continue
                            if not section_element.css.select_one('.row'):
                                continue

                            section = {
                                'name': section_element.css.select_one('h3').get_text().strip(),
                                'subsections': []
                            }

                            for subsection_element in section_element.css.select('.row > .col'):
                                subsection = {
                                    'name': subsection_element.css.select_one('h4').get_text().strip(),
                                    'entries': []
                                }

                                for entry_element in subsection_element.css.select('ul > li'):
                                    if 'class' in entry_element.parent.attrs and 'collapsable' in entry_element.parent.attrs['class']:
                                        continue

                                    link_element = entry_element.css.select_one('a')

                                    if link_element is not None:
                                        subsection_entry = {
                                            'name': link_element.get_text().strip().replace('\n', ' '),
                                            'href': link_element.attrs['href']
                                        }
                                    else:
                                        subsection_entry = {
                                            'name': entry_element.get_text().strip().replace('\n', ' '),
                                            'href': None
                                        }

                                    if entry_element.css.select_one('ul.collapsable'):
                                        subsection_entry['extras'] = []

                                        for extra_element in entry_element.css.select('ul.collapsable > li'):
                                            link_element = extra_element.css.select_one('a')

                                            if link_element is not None:
                                                subsection_entry['extras'].append({
                                                    'name': link_element.get_text().strip().replace('\n', ' '),
                                                    'href': link_element.attrs['href']
                                                })

                                    subsection['entries'].append(subsection_entry)

                                section['subsections'].append(subsection)

                            sections.append(section)

                        edition = Edition.objects.filter(year=edition_year).first()
                        if not edition:
                            edition = Edition(year=edition_year, name=edition_name)
                            edition.save()

                            # Generate settings from defaults
                            default_settings = EditionSetting.objects.filter(edition__isnull=True).all()
                            for default_setting in default_settings:
                                setting = EditionSetting(key=default_setting.key, value=default_setting.value, edition=edition)
                                setting.save()

                        edition.settings.filter(key='theme.hidden').update(value='false')

                        def create_puzzles(puzzle_entries, is_pregame: bool, puzzle_day: Optional[Day]):
                            for entry_index, entry in enumerate(puzzle_entries):
                                puzzle_name = entry['name'] if len(entry['name']) > 0 else f'Name unknown {entry_index + 1}'

                                puzzle = edition.puzzles.filter(name=puzzle_name).first()
                                if not puzzle:
                                    puzzle = Puzzle(name=puzzle_name, edition=edition)
                                    puzzle.save()

                                if is_pregame:
                                    if not hasattr(puzzle, 'pregame_code') or not puzzle.pregame_code:
                                        if not hasattr(edition, 'pregame') or not edition.pregame:
                                            pregame = Pregame(start=datetime(edition.year, 4, 1, 16, 0, 0),
                                                              end=datetime(edition.year, 4, 8, 16, 0, 0),
                                                              bonus_amount=0,
                                                              bonus_reason='Solved pregame',
                                                              edition=edition)
                                            pregame.save()
                                        else:
                                            pregame = edition.pregame

                                        pregame_code = PregamePuzzleCode(number=entry_index + 1, pregame=pregame, puzzle=puzzle)
                                        pregame_code.save()
                                else:
                                    if not hasattr(puzzle, 'code') or not puzzle.code:
                                        puzzle_code = PuzzleCode(number=entry_index + 1, day=puzzle_day, puzzle=puzzle)
                                        puzzle_code.save()

                                def create_puzzle_file(puzzle_file_type: PuzzleFile.Type, href: str):
                                    parsed_href = urllib.parse.unquote(href)
                                    file_path = Path(parsed_href)

                                    puzzle_file = puzzle.files.filter(type=puzzle_file_type, name=file_path.stem).first()
                                    if not puzzle_file:
                                        puzzle_file_info = find_info(parsed_href)

                                        with zip_file.open(puzzle_file_info, 'r') as puzzle_file_data:
                                            puzzle_file = PuzzleFile(type=puzzle_file_type, name=file_path.stem,
                                                                     file=DjangoFile(puzzle_file_data, name=file_path.name), puzzle=puzzle)
                                            puzzle_file.save()

                                if entry['href'] and entry['href'].startswith('archive/'):
                                    create_puzzle_file(PuzzleFile.Type.PUZZLE, entry['href'])

                                if 'extras' in entry:
                                    for extra_entry in entry['extras']:
                                        if extra_entry['href']:
                                            create_puzzle_file(PuzzleFile.Type.OTHER, extra_entry['href'])

                        def create_media_item(name: str, href: str, sort_index: int):
                            if href.startswith('http://') or href.startswith('https://'):
                                media_item = edition.media_items.filter(url=href)
                                if not media_item:
                                    media_item_type = EditionMediaItem.Type.OTHER
                                    if 'youtube.com/watch' in href:
                                        media_item_type = EditionMediaItem.Type.VIDEO

                                    media_item = EditionMediaItem(type=media_item_type, name=name, url=href, is_hidden=False, sort_index=sort_index,
                                                                  edition=edition)
                                    media_item.save()
                            else:
                                parsed_href = urllib.parse.unquote(href)
                                file_path = Path(parsed_href)

                                media_item = edition.media_items.filter(name=file_path.stem).first()
                                if not media_item:
                                    media_item_file_info = find_info(parsed_href)

                                    with zip_file.open(media_item_file_info, 'r') as media_item_file_data:
                                        media_item = EditionMediaItem(type=EditionMediaItem.Type.OTHER, name=name,
                                                                      file=DjangoFile(media_item_file_data, name=file_path.name),
                                                                      is_hidden=False, sort_index=sort_index, edition=edition)
                                        media_item.save()

                        for section in sections:
                            if section['name'] == 'Daily puzzles':
                                for subsection in section['subsections']:
                                    day_number = int(subsection['name'][4:])

                                    if edition_year not in START_DATE_BY_YEAR:
                                        raise ValidationError(f'No known start date for year {edition_year}.')

                                    edition_start = START_DATE_BY_YEAR[edition_year] + timedelta(days=day_number - 1)
                                    day_start = datetime.combine(edition_start, time(20, 0, 0))
                                    day_end = day_start + timedelta(days=1)

                                    day = edition.days.filter(number=day_number).first()
                                    if not day:
                                        day = Day(number=day_number, start=day_start, end=day_end, edition=edition)
                                        day.save()

                                    create_puzzles(subsection['entries'], False, day)
                            elif section['name'] == 'Other data':
                                for subsection_index, subsection in enumerate(section['subsections']):
                                    if subsection['name'] == 'Bonus':
                                        create_puzzles(subsection['entries'], False, None)
                                    elif subsection['name'] == 'Pregame':
                                        create_puzzles(subsection['entries'], True, None)
                                    else:
                                        for entry_index, entry in enumerate(subsection['entries']):
                                            if entry['href'] and entry['href'] != 'thegame.iapandora.html':
                                                create_media_item(
                                                    entry['name'] if subsection['name'] == entry['name'] else
                                                    '{} - {}'.format(subsection['name'], entry['name']),
                                                    entry['href'],
                                                    subsection_index * 10 + entry_index
                                                )

                        for score_row in score_rows:
                            if 'Team' in score_row or 'Company' in score_row:
                                team_name = score_row['Team'] if 'Team' in score_row else score_row['Company']

                                team = edition.teams.filter(name=team_name).first()
                                if not team:
                                    team = Team(name=team_name, edition=edition)
                                    team.save()

                                if 'Score' in score_row:
                                    archive_score = team.archive_scores.filter(type=ArchiveScore.Type.TOTAL).first()
                                    if not archive_score:
                                        archive_score = ArchiveScore(type=ArchiveScore.Type.TOTAL, score=int(score_row['Score']), team=team)
                                        archive_score.save()
                                else:
                                    for day_number in range(1, 5):
                                        day_key = f'Day {day_number}'
                                        if day_key in score_row:
                                            day = edition.days.filter(number=day_number).first()
                                            if not day:
                                                raise ValidationError(f'Day {day_number} for year {edition_year} does not exist.')

                                            archive_score = team.archive_scores.filter(type=ArchiveScore.Type.DAY, day=day).first()
                                            if not archive_score:
                                                archive_score = ArchiveScore(type=ArchiveScore.Type.DAY, score=int(score_row[day_key]), day=day, team=team)
                                                archive_score.save()

                                    if 'Bonus' in score_row:
                                        score = int(score_row['Bonus'])
                                        archive_score_type = ArchiveScore.Type.BONUS if score > 0 else ArchiveScore.Type.OFFENCE

                                        archive_score = team.archive_scores.filter(type=archive_score_type).first()
                                        if not archive_score:
                                            archive_score = ArchiveScore(type=archive_score_type, score=score, team=team)
                                            archive_score.save()

                                    if 'Pandollars' in score_row:
                                        archive_score = team.archive_scores.filter(type=ArchiveScore.Type.OTHER).first()
                                        if not archive_score:
                                            archive_score = ArchiveScore(type=ArchiveScore.Type.OTHER, score=int(score_row['']), team=team)
                                            archive_score.save()

        return super().form_valid(form)
