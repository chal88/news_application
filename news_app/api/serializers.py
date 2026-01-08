"""Serializers for the news app."""
from rest_framework import serializers
from news_app.models import Article, Publisher


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the Article model."""
    publisher = serializers.StringRelatedField()
    journalist = serializers.StringRelatedField()

    class Meta:
        """Meta class for ArticleSerializer."""
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'publisher',
            'journalist',
            'approved',
            'created_at',
        ]
        read_only_fields = fields


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for the Publisher model."""
    class Meta:
        """Meta class for PublisherSerializer."""
        model = Publisher
        fields = ['id', 'name']
