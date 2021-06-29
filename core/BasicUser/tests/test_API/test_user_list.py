"""Test the list user's API view."""
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser


class ListUserAPITest(APITestCase):
    """Test the List User API view."""

    def setUp(self):
            """Set up 30 users in the test DB."""
            for unused in range(30):
                create_user(model=get_user_model())

    def test_list_page_url(self):
        """Test the List User API view via URL."""
        response = self.client.get('/api/BasicUser/list/')
        self.assertEqual(response.status_code, 200)

    def test_list_page_view_name(self):
        """Test the List User API view view name."""
        response = self.client.get(reverse('api_list_users'))
        self.assertEqual(response.status_code, 200)

    # pagination tests
    def test_user_list_first_page(self):
        """Test that 1st page is paginated by 25 by default."""
        response = self.client.get(reverse('api_list_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 25)

    def test_user_list_last_page(self):
        """Test to ensure second page only has 5 user's."""
        response = self.client.get(reverse('api_list_users') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 5)
