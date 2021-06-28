"""Test for deleting a user via API."""
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser


class DeleteUserAPITest(APITestCase):
    """Test the delete user API.

    Attributes:
        client: The API client.
        user(TestBaseUser): The test user.
    """

    def setUp(self):
        """Set up the client and user."""
        self.client = APIClient()
        self.user = create_user(model=get_user_model())

    def test_delete_user_page_url(self):
        """Test the delete user URL."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/api/BasicUser/delete/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_page_view_name(self):
        """Test the delete user URL."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('api_delete_user'))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_receives_401(self):
        """Test the delete user URL."""
        response = self.client.delete(reverse('api_delete_user'))
        self.assertEqual(response.status_code, 401)

    def test_expected_data(self):
        """Test the response of delete user API."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('api_delete_user'))

        self.assertIn('Success', response.data)
        self.assertTrue('User has been deleted', response.data['Success'])
        self.assertEqual(BasicUser.objects.all().count(), 0)
