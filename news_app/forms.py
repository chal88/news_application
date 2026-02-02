"""Forms for user registration and authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Article, PublishingHouse, Newsletter
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class UserRegisterForm(forms.ModelForm):
    """
    Public registration form for Reader, Journalist and editor users only.
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
            ("editor", "Editor"),
        ]
    )

    publishing_house = forms.ModelChoiceField(
        queryset=PublishingHouse.objects.all(),
        required=False,
        empty_label="Select Publishing House (Journalists and Editors only)",
    )

    new_publishing_house = forms.CharField(
        required=False,
        label="Or add a new Publishing House",
        help_text="Only required if your publishing house is not listed"
    )

    class Meta:
        """Meta class for UserRegisterForm."""
        model = CustomUser
        fields = [
            "username",
            "email",
            "role",
            "publishing_house",
            "new_publishing_house",
            "password1",
            "password2",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        role = cleaned_data.get("role")
        publishing_house = cleaned_data.get("publishing_house")
        new_publishing_house = cleaned_data.get("new_publishing_house")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        if (
            role in ["journalist", "editor"]
            and not (publishing_house or new_publishing_house)
        ):
            raise forms.ValidationError(
                "Journalists and editors must select a publishing house."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Set password correctly
        user.set_password(self.cleaned_data["password1"])

        role = self.cleaned_data.get("role")
        publishing_house = self.cleaned_data.get("publishing_house")
        new_publishing_house = self.cleaned_data.get("new_publishing_house")

        # If user entered a new publishing house, create it
        if new_publishing_house:
            publishing_house, _ = PublishingHouse.objects.get_or_create(
                name=new_publishing_house.strip()
            )

        # Assign publishing house ONLY to journalist/editor
        if role in ["journalist", "editor"]:
            user.publishing_house = publishing_house

        if commit:
            user.save()

        return user


class NewsletterForm(forms.ModelForm):
    """Form for creating or updating a newsletter."""
    class Meta:
        """Meta class for NewsletterForm."""
        model = Newsletter
        fields = ["title", "content"]


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
