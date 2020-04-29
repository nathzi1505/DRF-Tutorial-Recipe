from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Ingredient, Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def sample_ingredient(user, name="Cinnamon"):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_tag(user, name="Main Course"):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 10,
        "price": 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipesApiTests(TestCase):
    """Test the publicly available recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="john.doe@example.com",
            password="johndoe12345"
        )
        self.client.force_authenticate(self.user)

    def test_filter_recipes_by_tags(self):
        """Test returning recipes with specific tags"""
        recipe1 = sample_recipe(user=self.user, title="Thai Vegetable Curry")
        recipe2 = sample_recipe(user=self.user, title="Aubergine with Tahini")
        tag1 = sample_tag(user=self.user, name="Vegan")
        tag2 = sample_tag(user=self.user, name="Vegetarian")
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag2)
        recipe3 = sample_recipe(user=self.user, title="Fish and Chips")

        res = self.client.get(
            RECIPES_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_recipes_by_ingredients(self):
        """Test returning recipes with specific ingredients"""
        recipe1 = sample_recipe(user=self.user, title="Posh Beans on Toast")
        recipe2 = sample_recipe(user=self.user, title="Chicken Cacciatore")
        ingredient1 = sample_ingredient(user=self.user, name="Feta Cheese")
        ingredient2 = sample_ingredient(user=self.user, name="Chicken")
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)
        recipe3 = sample_recipe(user=self.user, title="Steak and Mushrooms")

        res = self.client.get(
            RECIPES_URL,
            {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
        )

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
