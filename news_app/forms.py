"""Forms for user registration and authentication.
"""
from django import forms
from .models import CustomUser
from .models import Article, PublishingHouse, Newsletter


class UserRegisterForm(forms.ModelForm):
    """Form for registering Reader, Journalist, and Editor users."""

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
        empty_label="Select Publishing House (Journalists only)"
    )

    new_publishing_house = forms.CharField(
        required=False,
        label="Or add new publishing house (Editors only)"
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
        """Custom validation for passwords and publishing house logic."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        role = cleaned_data.get("role")
        publishing_house = cleaned_data.get("publishing_house")
        new_publishing_house = cleaned_data.get("new_publishing_house")

        # Validate password match
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        # Validate publishing house rules
        if role == "journalist":
            if not publishing_house:
                raise forms.ValidationError(
                    "Journalists must select an existing publishing house."
                )
            if new_publishing_house:
                raise forms.ValidationError(
                    "Journalists cannot create a new publishing house."
                )

        if role == "editor":
            if not publishing_house and not new_publishing_house:
                raise forms.ValidationError(
                    "Editors must select an existing publishing house"
                    " or create a new one."
                )

        return cleaned_data

    def save(self, commit=True):
        """
        Override save method to hash password and assign publishing house.
         Depending on the role, either assign an existing publishing house
         or create a new one for editors."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        role = self.cleaned_data.get("role")
        new_ph_name = self.cleaned_data.get("new_publishing_house")
        existing_ph = self.cleaned_data.get("publishing_house")

        # Assign publishing house
        if role == "editor" and new_ph_name:
            # Editors can create new publishing house
            publishing_house, _ = PublishingHouse.objects.get_or_create(
                name=new_ph_name
            )
            user.publishing_house = publishing_house
        else:
            # For journalists or editors selecting existing
            user.publishing_house = existing_ph

        if commit:
            user.save()

        return user


class NewsletterForm(forms.ModelForm):
    """Form to handle creating and updating newsletters, allowing users
    to specify title and content.
    """
    class Meta:
        """Meta class for NewsletterForm."""
        model = Newsletter
        fields = ["title", "content"]


class ArticleForm(forms.ModelForm):
    """
    Form for creating or updating an article.
    Automatically assigns author and publishing house.
    """

    publishing_house = forms.ModelChoiceField(
        queryset=PublishingHouse.objects.all(),
        required=False,
        empty_label="Use my publishing house"
    )

    class Meta:
        model = Article
        fields = ["title", "content", "publishing_house"]

    def __init__(self, *args, **kwargs):
        # Expect request to be passed in from the view
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        article = super().save(commit=False)

        # Always assign the logged-in journalist as author
        if self.request:
            article.author = self.request.user

            # Auto-assign publishing house if not explicitly chosen
            if not article.publishing_house:
                article.publishing_house = self.request.user.publishing_house

        if commit:
            article.save()

        return article
