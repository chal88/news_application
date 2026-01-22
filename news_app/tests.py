"""Unit tests for user registration, role assignment, and article workflow. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Article

User = get_user_model()


class UserRegistrationTest(TestCase):
    """Tests for user registration functionality."""
    def test_user_can_register(self):
        """Test that a user can register successfully."""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'reader',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserRoleAssignmentTest(TestCase):
    """Tests for user role assignment upon registration."""
    def test_user_is_assigned_correct_group(self):
        """Test that a user is assigned to the correct group based on role."""
        user = User.objects.create_user(
            username='journalist1',
            password='password123',
            role='journalist'
        )

        self.assertTrue(user.groups.filter(name='Journalist').exists())


class ArticleWorkflowTest(TestCase):
    """Tests for article submission and approval workflow."""
    def setUp(self):
        self.journalist = User.objects.create_user(
            username='journalist_user',
            password='password123',
            role='journalist'
        )

        self.editor = User.objects.create_user(
            username='editor_user',
            password='password123',
            role='editor'
        )

    def test_journalist_can_submit_article(self):
        """Test that a journalist can submit an article."""
        article = Article.objects.create(
            title='Test Article',
            content='Article content',
            journalist=self.journalist,
            approved=False
        )

        self.assertEqual(article.journalist, self.journalist)
        self.assertFalse(article.approved)

    def test_editor_can_approve_article(self):
        """Test that an editor can approve an article."""
        article = Article.objects.create(
            title='Pending Article',
            content='Pending content',
            journalist=self.journalist,
            approved=False
        )

        article.approved = True
        article.save()

        self.assertTrue(article.approved)
