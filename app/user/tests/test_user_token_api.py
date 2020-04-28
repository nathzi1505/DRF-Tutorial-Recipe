from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users token api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            "email": "jane.doe@example.com",
            "password": "janedoe54321",
            "name": "Jane Doe"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""

        create_user(**{"email": "jane.doe@example.com",
                       "password": "janedoe54321", "name": "Jane Doe"})

        payload = {
            "email": "jane.doe@example.com",
            "password": "wrong_password"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            "email": "jane.doe@example.com",
            "password": "janedoe54321",
            "name": "Jane Doe"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password is requirement"""
        res = self.client.post(TOKEN_URL, {"email": 'one', "password": ""})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
