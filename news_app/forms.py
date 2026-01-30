"""Forms for user registration and authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Article, PublishingHouse
from django.contrib.auth.hashers import make_password


class UserRegisterForm(forms.ModelForm):
    """
    Public registration form for Reader and Journalist users only.
    Editors are created by Admin.
    """

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

    publishing_house = forms.ModelChoiceField(
        queryset=PublishingHouse.objects.all(),
        required=False,
        empty_label="Select Publishing House (Journalists only)"
    )

    class Meta:
        """Meta class for UserRegisterForm."""
        model = CustomUser
        fields = [
            "username",
            "email",
            "role",
            "publishing_house",
            "password1",
            "password2",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        role = cleaned_data.get("role")
        publishing_house = cleaned_data.get("publishing_house")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        if role == "journalist" and not publishing_house:
            raise forms.ValidationError(
                "Journalists must select a publishing house."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()

        return user


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

