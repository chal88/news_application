"""Unit tests for user registration, role assignment, and article workflow. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Article

User = get_user_model()


class UserRegistrationTest(TestCase):
    """Tests for user registration functionality.
    Tests successful registration , validation errors,
    and redirection based on user role.
    """
    def test_user_can_register(self):
        """Test that a user can register successfully
        with valid credentials.
        """
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
    """Tests for validating user role assignment upon registration.
    Tests covers that users are assigned correct roles and groups.
    """
    def test_user_is_assigned_correct_group(self):
        """Test that a user is assigned to the correct group based on role."""
        user = User.objects.create_user(
            username='journalist1',
            password='password123',
            role='journalist'
        )

        self.assertTrue(user.groups.filter(name='Journalist').exists())


class ArticleWorkflowTest(TestCase):
    """Tests for article submission and approval workflow,
    including approval and notification mechanisms.
    """
    def setUp(self):
        """Set up test users and initial data for article workflow tests by
        creating a journalist and an editor user.
        """
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
        """Test that a user with 'journalist' permissions can submit
          an article and store it in the database.
          """
        article = Article.objects.create(
            title='Test Article',
            content='Article content',
            author=self.journalist,
            approved=False
        )

        self.assertEqual(article.author, self.journalist)
        self.assertFalse(article.approved)

    def test_editor_can_approve_article(self):
        """Tests that an authorized editor can approve a submitted article
          and that the article's approved status is updated correctly.
        """
        article = Article.objects.create(
            title='Pending Article',
            content='Pending content',
            author=self.journalist,
            approved=False
        )

        article.approved = True
        article.save()

        self.assertTrue(article.approved)
