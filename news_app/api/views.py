"""
API views for the news app.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from news_app.models import PublishingHouse, Article
from news_app.api.serializers import (
    PublishingHouseSerializer,
    ArticleSerializer,
)
from rest_framework import generics


class SubscribedArticlesAPIView(APIView):
    """
    Returns approved articles based on reader subscriptions.
    Only accessible to authenticated readers.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns approved articles based on reader subscriptions.
        Only accessible to authenticated readers.
        """
        user = request.user

        # Ensure only readers can access the API
        if user.role != "reader":
            raise PermissionDenied("Only readers can access this endpoint.")

        # Use publishing_house instead of publisher
        articles = Article.objects.filter(
            approved=True
        ).filter(
            Q(publishing_house__in=user.subscribed_publishing_houses.all()) |
            Q(journalist__in=user.subscribed_journalists.all())
        ).distinct()

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class PublishingHouseListView(generics.ListAPIView):
    """List all publishing houses."""
    queryset = PublishingHouse.objects.all()
    serializer_class = PublishingHouseSerializer

