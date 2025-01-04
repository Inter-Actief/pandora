from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView, WellKnownMicrosoftView

urlpatterns = [
    path('accounts/profile/', ProfileDetailView.as_view(), name='account_profile'),
    path('accounts/profile/update', ProfileUpdateView.as_view(), name='account_profile_update'),

    path('.well-known/microsoft-identity-association.json', WellKnownMicrosoftView.as_view())
]
