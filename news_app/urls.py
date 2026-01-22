"""API URL configurations for the news application."""
from django.urls import path
from .views import (
    user_login,
    user_logout,
    article_list,
    pending_articles,
    approve_article,
    journalist_dashboard,
    submit_article,
    article_detail
)
from . import views

urlpatterns = [
    path("", article_list, name="article_list"),
    path(" ", views.home, name="home"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

    path("editor/pending/", pending_articles, name="pending_articles"),
    path("editor/approve/<int:article_id>/", approve_article,
         name="approve_article"),

    path("journalist/dashboard/", journalist_dashboard,
         name="journalist_dashboard"),
    path("journalist/submit/", submit_article, name="submit_article"),
    path(
        "articles/<int:article_id>/",
        article_detail,
        name="article_detail"),
    path('register/', views.register, name='register'),


]
