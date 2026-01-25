"""Models for the news application, including 
custom user roles and articles."""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class PublishingHouse(models.Model):
    """A publishing house that journalists and editors belong to."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class CustomUser(AbstractUser):
    """Custom user model with roles."""

    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    publishing_house = models.ForeignKey(
        PublishingHouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Required for editors and journalists only"
    )

    def __str__(self):
        return str(self.username)


class Article(models.Model):
    """News article model."""

    title = models.CharField(max_length=200)
    content = models.TextField()

    journalist = models.ForeignKey(
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)




from django.db import models


