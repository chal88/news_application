"""Admin configuration for the news app."""
from django.contrib import admin
from .models import Publisher, CustomUser, Article

admin.site.register(Publisher)
admin.site.register(CustomUser)
admin.site.register(Article)
