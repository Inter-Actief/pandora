from allauth.account.forms import LoginForm as AllAuthLoginForm, SignupForm as AllAuthSignupForm
from django import forms


class LoginForm(AllAuthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = None


class SignupForm(AllAuthSignupForm):
    first_name = forms.CharField(label='First name', min_length=1)
    last_name = forms.CharField(label='Last name', min_length=1)
