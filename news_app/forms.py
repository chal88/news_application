"""Forms for user registration and authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Article, PublishingHouse


from django import forms
from .models import CustomUser

class UserRegisterForm(forms.ModelForm):
    """Form for registering Reader and Journalist users only"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    role = forms.ChoiceField(
        choices=[
            ("reader", "Reader"),
            ("journalist", "Journalist"),
        ]
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class ArticleForm(forms.ModelForm):
    """Form for creating or updating an article with 
    optional publishing house selection."""
    publishing_house = forms.ModelChoiceField(
        queryset=PublishingHouse.objects.all(),
        required=False,
        empty_label="Independent (No publishing house)"
    )

    class Meta:
        """Meta class for ArticleForm."""
        model = Article
        fields = ["title", "content", "publishing_house"]

