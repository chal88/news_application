"""Models for the news application, including custom user model with roles
and subscriptions."""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Publisher(models.Model):
    """Model representing a news publisher."""
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class CustomUser(AbstractUser):
    """Custom user model with roles and subscription capabilities."""
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    subscribed_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name='subscribers'
    )

    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers'
    )

    def __str__(self):
        return str(self.username)


class Article(models.Model):
    """Model representing a news article."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    journalist = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
