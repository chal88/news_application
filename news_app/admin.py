"""Admin configurations for news_app models."""
from django.contrib import admin
from .models import CustomUser, PublishingHouse, Article, Newsletter

# --------------------------------------
# Register CustomUser
# --------------------------------------


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin interface for the custom User model.
    Provides customized user management, including list display,
    fieldsets for editing, search capabilities, and filtering
    options tailored to the CustomUser model's fields.
    """
    list_display = ("username", "email", "role", "publishing_house",
                    "is_staff", "is_active")
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
    """Admin interface options for PublishingHouse model.
    Allows management of publishing houses with list display,
    search functionality, and ordering for publishing houses 
    within the Django admin panel.

    """
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

# --------------------------------------
# Register Article
# --------------------------------------


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin interface customization for Article model.
    Enables management of articles with options for list display,
    filtering, searching, and ordering within the Django admin panel.
    """
    list_display = ("title", "author", "publishing_house",
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
    """Admin interface for managing Newsletter model.
    Provides list display, search functionality, ordering,
    and read-only fields for effective newsletter management
    within the Django admin panel.
    """
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
