from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView

from pandora.editions.forms.edition import EditionCreateForm
from pandora.editions.mixins import CommitteeMemberAccessMixin, EditionMixin
from pandora.editions.models import Edition


class EditionCreateView(CommitteeMemberAccessMixin, CreateView):
    model = Edition
    form_class = EditionCreateForm
    template_name_suffix = '_create'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()

        now = timezone.now()
        initial['year'] = now.year
        initial['start'] = now.date() + timedelta(days=7)
        initial['pregame_start'] = now.date() + timedelta(days=1)

        return initial

    def get_success_url(self):
        return reverse('committee_dashboard',  kwargs={'year': self.object.year})


class ParticipantEditionDetailView(EditionMixin, DetailView):
    model = Edition
    template_name = 'editions/participant_edition_detail.html'
    context_object_name = 'edition'

    def get_object(self, queryset=None):
        return self.get_edition()
