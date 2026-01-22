# news_app/signals.py
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import send_mail
import requests
from django.db import models
from .models import Article, CustomUser
import tweepy
import logging

try:
    import tweepy
except ImportError:
    tweepy = None


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    """Create user groups and assign permissions after migrations."""
    if sender.name != 'news_app':
        return
    reader_group, _ = Group.objects.get_or_create(name='Reader')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')

    article_ct = ContentType.objects.get_for_model(Article)

    view_article = Permission.objects.get(codename='view_article',
                                          content_type=article_ct)
    add_article = Permission.objects.get(codename='add_article',
                                         content_type=article_ct)
    change_article = Permission.objects.get(codename='change_article',
                                            content_type=article_ct)
    delete_article = Permission.objects.get(codename='delete_article',
                                            content_type=article_ct)

    reader_group.permissions.set([view_article])
    editor_group.permissions.set([view_article, change_article,
                                  delete_article])
    journalist_group.permissions.set([view_article, add_article,
                                      change_article, delete_article])


@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    """Assign user to a group based on their role after creation."""
    if not created:
        return

    group_map = {
        'reader': 'Reader',
        'editor': 'Editor',
        'journalist': 'Journalist'
    }

    group_name = group_map.get(instance.role)
    if group_name:
        try:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass


@receiver(post_save, sender=Article)
def notify_on_article_approval(sender, instance, created, **kwargs):
    """Send notifications when an article is approved."""
    if not instance.approved or instance.notified:
        return

    subscribed_readers = CustomUser.objects.filter(
        role='reader'
    ).filter(
        models.Q(subscribed_publishers=instance.publisher) |
        models.Q(subscribed_journalists=instance.journalist)
    ).distinct()

    email_list = [user.email for user in subscribed_readers if user.email]

    if email_list:
        send_mail(
            subject=f"New Article Published: {instance.title}",
            message=f"""
A new article has been published.

Title: {instance.title}
Author: {instance.journalist.username}

{instance.content[:300]}...
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email_list,
            fail_silently=True,
        )

    post_to_x(instance)
    Article.objects.filter(id=instance.id).update(notified=True)


logger = logging.getLogger(__name__)


def post_to_x(article):
    """Posts article summary to X using OAuth 1.0a."""
    try:
        client = tweepy.Client(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        )

        tweet_text = f"📰 {article.title}\n\n{article.content[:200]}..."
        client.create_tweet(text=tweet_text)

        logger.info("Article successfully posted to X")

    except Exception:
        logger.exception("Failed to post article to X")
        raise
    if tweepy is None:
        logger.warning("Tweepy not installed; skipping X post")
        return