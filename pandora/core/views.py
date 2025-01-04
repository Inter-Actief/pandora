import json

from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import SocialApp
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name')
    template_name = 'account/profile_update.html'
    success_url = reverse_lazy('account_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        get_adapter(self.request).add_message(
            self.request,
            messages.INFO,
            'account/messages/profile_changed.txt'
        )
        return response


class WellKnownMicrosoftView(View):

    def get(self, request):
        social_apps = SocialApp.objects.filter(provider='microsoft').all()

        return HttpResponse(
            content=json.dumps({
                'associatedApplications': [
                    {
                        'applicationId': social_app.client_id
                    } for social_app in social_apps
                ]
            }),
            headers={
                'Content-Type': 'application/json'
            }
        )
