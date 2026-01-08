"""
API views for the news app.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from news_app.models import Article
from .serializers import ArticleSerializer


class SubscribedArticlesAPIView(APIView):
    """
    Returns approved articles based on reader subscriptions.
    Only accessible to authenticated readers.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Ensure only readers can access the API
        if user.role != "reader":
            raise PermissionDenied("Only readers can access this endpoint.")

        articles = Article.objects.filter(
            approved=True
        ).filter(
            Q(publisher__in=user.subscribed_publishers.all()) |
            Q(journalist__in=user.subscribed_journalists.all())
        ).distinct()

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
