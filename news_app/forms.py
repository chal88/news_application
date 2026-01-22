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

    def __init__(self, *args, **kwargs):
        # Pop the 'current_user' from kwargs (we’ll pass it from view)
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Allow editor role only if the current user is superuser
        if current_user and current_user.is_superuser:
            self.fields['role'].choices.append(('editor', 'Editor'))
