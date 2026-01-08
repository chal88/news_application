"""news_project/news_app/api/urls.py"""
from django.urls import path
from .views import SubscribedArticlesAPIView

urlpatterns = [
    path(
        "articles/",
        SubscribedArticlesAPIView.as_view(),
        name="api_articles"
    ),
]
