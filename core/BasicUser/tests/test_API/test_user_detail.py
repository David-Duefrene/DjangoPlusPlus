"""Test the user detail API view."""
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from BasicUser.models import BasicUser
from TestUtil.create_user import create_user


class UserDetailAPITest(APITestCase):
    """Test the user detail API."""

    def setUp(self):
        """Set up a user in the test DB."""
        self.user = create_user(model=get_user_model())

    def test_detail_page_url(self):
        """Test the BasicUserDetail API view via URL returns HTTP 200."""
        response = self.client.get("/api/BasicUser/view/1")
        self.assertEqual(response.status_code, 200)

    def test_detail_page_view_name(self):
        """Test the BasicUserDetail API view name returns HTTP 200."""
        response = self.client.get(reverse('api_view_user', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_expected_data(self):
        """Test the User detail API returns expected data."""
        response = self.client.get(reverse('api_view_user', kwargs={'pk': '1'}))

        # username
        self.assertIn('username', response.data)
        self.assertTrue(self.user.username, response.data['username'])

        # email
        self.assertIn('email', response.data)
        self.assertTrue(self.user.email, response.data['email'])

        # first name
        self.assertIn('first_name', response.data)
        self.assertTrue(self.user.first_name, response.data['first_name'])

        # last name
        self.assertIn('last_name', response.data)
        self.assertTrue(self.user.last_name, response.data['last_name'])

        # absolute URL
        self.assertIn('get_absolute_url', response.data)
        self.assertTrue(self.user.get_absolute_url, response.data['get_absolute_url'])
