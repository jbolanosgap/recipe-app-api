"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from core import models


def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_superuser(**params)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email, password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='', password='test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_superuser(
            email='test@example.com',
            password='test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test successful creation of a recipe"""

        user = create_user(
            email='test@example.com',
            password='test123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Steak and Mushroom Sauce',
            time_minutes=5,
            price=Decimal('5.50'),
            description='A delicious steak with mushroom sauce'
        )

        self.assertEqual(str(recipe), recipe.title)
        self.assertIsNotNone(recipe.id)

    def test_create_tag(self):
        """Test creating a tag"""
        user = create_user(
            email='test@example.com',
            password='test123'
        )
        tag = models.Tag.objects.create(
            user=user,
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

        self.assertGreater(models.Tag.objects.count(), 0)
