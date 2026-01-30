"""Admin configurations for news_app models."""
from django.contrib import admin
from .models import CustomUser, PublishingHouse, Article, Newsletter

# --------------------------------------
# Register CustomUser
# --------------------------------------


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin for CustomUser model."""
    list_display = ("username", "email", "role", "publishing_house", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active", "publishing_house")
    search_fields = ("username", "email")
    ordering = ("username",)
    # prevent editing password here
    readonly_fields = ("password",)

# --------------------------------------
# Register PublishingHouse
# --------------------------------------


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    """Admin for PublishingHouse model."""
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

# --------------------------------------
# Register Article
# --------------------------------------


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin for Article model."""
    list_display = ("title", "journalist", "publishing_house",
                    "approved", "created_at")
    list_filter = ("approved", "publishing_house")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

# --------------------------------------
# Register Newsletter
# --------------------------------------


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin for Newsletter model."""
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
