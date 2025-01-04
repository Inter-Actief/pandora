from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import FormView, ListView, View

from pandora.editions.forms.kill_code import KillCodeGenerateForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import KillCode, Kill
from pandora.editions.resources.kill_code import KillCodeResource


class KillCodeListView(EditionMixin, CommitteeMemberAccessMixin, ListView):
    model = KillCode
    context_object_name = 'kill_codes'

    def get_queryset(self):
        day = self.edition.days.get(number=self.kwargs.get('day_number'))
        if not day:
            return Kill.objects.none()
        return day.kill_codes.order_by('team_member__team__name', 'team_member__name')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['day'] = self.edition.days.get(number=self.kwargs.get('day_number'))
        return context_data


class KillCodeGenerateView(EditionMixin, CommitteeMemberAccessMixin, FormView):
    form_class = KillCodeGenerateForm
    template_name = 'editions/killcode_generate.html'

    def get_success_url(self):
        return reverse('kill_codes', kwargs={'year': self.edition.year, 'day_number': 1})

    @transaction.atomic
    def form_valid(self, form):
        # Delete existing kill codes
        KillCode.objects.filter(day__edition=self.edition).delete()

        # Find days and active team members
        days = self.edition.days.order_by('number').all()
        team_members = self.edition.active_team_members.all()

        # Generate new kill codes
        for day in days:
            for team_member in team_members:
                kill_code = KillCode(day=day, team_member=team_member)
                kill_code.save()

        return super().form_valid(form)


class KillCodeExportView(EditionMixin, CommitteeMemberAccessMixin, View):

    def get(self, request, *args, **kwargs):
        day = self.edition.days.get(number=self.kwargs.get('day_number'))

        dataset = KillCodeResource().export(day.kill_codes.order_by('team_member__team__name', 'team_member__name'))

        file_name = f'{self.edition.year}_day_{day.number}_kill_codes.csv'
        file_content = dataset.csv

        response = HttpResponse(file_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
