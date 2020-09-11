from django.conf import settings
from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from allauth.account.adapter import DefaultAccountAdapter


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).count():
            raise forms.ValidationError('This username has already been taken!')

        domain = email.split('@')[1]

        if domain != settings.EMAIL_ALLOWED_DOMAIN:
            raise forms.ValidationError('Invalid domain, check your email address')

        return email
