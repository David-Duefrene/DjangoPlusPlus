"""Test the change password API."""
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser


class ChangePasswordAPITest(APITestCase):
    """Test the Change Password API.

    Attributes:
        user: A test user

    Methods:
        setUp: sets the test user
    """

    def setUp(self):
        """Create a user and login data."""
        self.user = create_user(model=BasicUser)

    def test_fails_missing_password_fields(self):
        """Test no password fails.

        Tests that response data contains ErrorDetail for password if missing
        password.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('api_change_password'), {})
        error = [ErrorDetail(string='This field is required.',
                             code='required')]

        self.assertEqual(response.data['old_password'], error)
        self.assertEqual(response.data['new_password'], error)

    def test_can_change_password(self):
        """Test correct data allows passwords to be changed.

        Tests that response data contains a success status and correct message.
        Also ensures the server return code 200.
        """
        data = {"old_password": 'password', "new_password": "newpw"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('api_change_password'), data)

        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         'Password updated successfully')
        self.assertEqual(response.status_code, 200)

    def test_change_password_page_url(self):
        """Test the change password API view via URL."""
        response = self.client.put("/api/BasicUser/change_password/")
        self.assertEqual(response.status_code, 302)

    def test_change_password_page_view_name(self):
        """Test the change password view name."""
        response = self.client.put(reverse('api_change_password'))
        self.assertEqual(response.status_code, 302)
