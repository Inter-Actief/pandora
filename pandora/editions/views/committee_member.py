from django.views.generic import ListView

from pandora.editions.mixins import EditionMixin
from pandora.editions.models import CommitteeMember


class CommitteeMemberListView(EditionMixin, ListView):
    model = CommitteeMember
    context_object_name = 'committee_members'

    def get_queryset(self):
        return self.edition.committee_members.filter(is_hidden=False).order_by('sort_index', 'function')
