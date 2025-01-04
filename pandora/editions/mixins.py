from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import redirect

from pandora.editions.models import Edition


class EditionMixin:

    kwargs: dict[str, Any]
    edition: Edition

    def get_edition(self):
        if 'year' in self.kwargs:
            return Edition.objects.get(year=self.kwargs.get('year'))
        elif 'edition_id' in self.kwargs:
            return Edition.objects.get(id=self.kwargs.get('edition_id'))
        return Edition.get_latest()

    def dispatch(self, request, *args, **kwargs):
        try:
            self.edition = self.get_edition()
        except Edition.DoesNotExist:
            return redirect('edition_create')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edition'] = self.edition
        return context


class CommitteeMemberAccessMixin(LoginRequiredMixin, UserPassesTestMixin):

    request: HttpRequest
    edition: Edition

    def test_func(self):
        return self.edition.committee_members.filter(user=self.request.user).exists()
