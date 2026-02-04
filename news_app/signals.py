"""Django signals for the news application.
"""
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
    """
    Create user groups and assign permissions after migrations.
    This signal ensures that the necessary groups (Reader, Editor, Journalist)
    and their permissions are set up. It checks if the sender
    is the news_app to avoid running during unrelated migrations.
    The permissions for viewing, adding, changing, and deleting articles are
    assigned according to the role of each group.
    """
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


# @receiver(post_save, sender=CustomUser)
# def assign_groups(sender, instance, created, **kwargs):
#     """Assign users to groups based on their role upon creation."""
#     if created:
#         if instance.role == "editor":
#             instance.is_staff = True
#             instance.is_active = False  # must be approved
#             instance.save()


@receiver(post_save, sender=Article)
def notify_on_article_approval(sender, instance, created, **kwargs):
    """Send notifications when an article is approved.
    This signal is triggered after an Article instance is saved.
    It checks if the article is approved and not yet notified. If so,
    it sends email notifications to all readers subscribed to the article's
    publisher or author. It also posts a summary of the article to X.
    """
    if not instance.approved or instance.notified:
        return

    subscribed_readers = CustomUser.objects.filter(
        role='reader'
    ).filter(
        models.Q(subscribed_publishers=instance.publisher) |
        models.Q(subscribed_authors=instance.author)
    ).distinct()

    email_list = [user.email for user in subscribed_readers if user.email]

    if email_list:
        send_mail(
            subject=f"New Article Published: {instance.title}",
            message=f"""
A new article has been published.

Title: {instance.title}
Author: {instance.author.username}

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
    """Posts article summary to X(formerly Twitter) using OAuth 1.0a
    API credentials must be set in settings.py and tweepy must be installed.
    An exception is logged if posting fails and the function exits gracefully if
    tweepy is not available.
    """
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