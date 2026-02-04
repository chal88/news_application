"""Models for the news application, including 
custom user roles and articles."""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class PublishingHouse(models.Model):
    """Represents a publishing house that journalists and editors belong to
    and that articles are associated with.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """String representation of the publishing house."""
        return str(self.name)


class CustomUser(AbstractUser):
    """Custom user model with roles and optional association to a
    publishing house for journalists and editors only.
    """

    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=False,
        blank=False,
        )

    publishing_house = models.ForeignKey(
        PublishingHouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Required for editors and journalists only"
    )

    def __str__(self):
        """String representation of the user to
            include username and role for clarity.
            """
        return str(self.username)


class Article(models.Model):
    """Represents a news article entry with title, content, author,
    and approval status. These articles are created by journalists
    and can be approved by editors."""

    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"},
        related_name="articles"
    )

    publishing_house = models.ForeignKey(
        PublishingHouse,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles"
    )

    approved = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the article to include title for clarity.
        """
        return str(self.title)


class Newsletter(models.Model):
    """Represents a newsletter model for periodic updates
    created by journalists and optionally associated with a publishing house.
    This model stores the title, content, author, and creation date 
    of the newsletter."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the newsletter to include
        title for clarity."""
        return str(self.title)
