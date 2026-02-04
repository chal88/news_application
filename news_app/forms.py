"""Forms for user registration and authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Article, PublishingHouse, Newsletter
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


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

    publishing_house = forms.ModelChoiceField(
        queryset=PublishingHouse.objects.all(),
        required=False,
        empty_label="Select Publishing House (Journalists only)"
    )

    new_publishing_house = forms.CharField(
        required=False,
        label="Or add new publishing house"
    )

    class Meta:
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
        new_publishing_house = cleaned_data.get("new_publishing_house")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        if role == "journalist" and not publishing_house and not new_publishing_house:
            raise forms.ValidationError(
                "Journalists must select or create a publishing house."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # ✅ IMPORTANT: hash password correctly
        user.set_password(self.cleaned_data["password1"])

        # Handle publishing house creation
        new_ph_name = self.cleaned_data.get("new_publishing_house")
        if new_ph_name:
            publishing_house, _ = PublishingHouse.objects.get_or_create(
                name=new_ph_name
            )
            user.publishing_house = publishing_house
        else:
            user.publishing_house = self.cleaned_data.get("publishing_house")

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
