"""Forms for user registration and authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Form for registering a new user with an additional role field."""
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        """Meta class for UserRegisterForm."""
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        