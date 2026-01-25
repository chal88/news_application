"""
Admin configuration for the news application.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Article, PublishingHouse

# ---------------------------------------
# CUSTOM USER ADMIN
# ---------------------------------------

# Unregister first if already registered to avoid AlreadyRegistered error
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model."""
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff',
                    'is_superuser']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'publishing_house')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role', 'publishing_house')}),
    )

# Register CustomUser with the admin site


admin.site.register(CustomUser, CustomUserAdmin)

# ---------------------------------------
# ARTICLE ADMIN
# ---------------------------------------


class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model."""
    list_display = ['title', 'journalist', 'approved', 'created_at',
                    'publishing_house']
    list_filter = ['approved', 'created_at', 'publishing_house']
    search_fields = ['title', 'content', 'journalist__username']
    ordering = ['-created_at']


admin.site.register(Article, ArticleAdmin)

# ---------------------------------------
# PUBLISHING HOUSE ADMIN
# ---------------------------------------


class PublishingHouseAdmin(admin.ModelAdmin):
    """Admin configuration for PublishingHouse model."""
    list_display = ['name', 'get_editor_username']
    search_fields = ['name', 'editor__username']

    def get_editor_username(self, obj):
        """Return the username of the editor
        associated with the publishing house."""
        editor = obj.customuser_set.filter(role='editor').first()
        return editor.username if editor else "-"


admin.site.register(PublishingHouse, PublishingHouseAdmin)
