"""Test the register API."""
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail

from BasicUser.models import BasicUser


class RegisterAPITest(APITestCase):
    """Test the Register API.

    Attributes:
        user_data(dict): A user's data.
        BlankFieldError: The error that will be received if a required field.
            is blank.

    Methods:
        setUp(self): resets the user_data every test.
        register(self): registers the user with user_data.

    Tests:
        test_can_create_account
        test_can_create_account_with_first_name
        test_can_create_account_with_email
        test_fails_missing_username
        test_fails_missing_password
    """

    def setUp(self):
        """Set up the user data."""
        self.user_data = {
            'username': 'test', 'email': '',
            'password': 'nrf6V2', 'first_name': ''
        }
        self.BlankFieldError = [ErrorDetail(
            string='This field may not be null.', code='null')]

    def register(self):
        """Register a user via post.

        Returns: server response.
        """
        return self.client.post(
            reverse('api_create_user'), self.user_data, format='json')

    def test_can_create_account(self):
        """Tests that we can create an account."""
        self.register()
        self.assertTrue(
            BasicUser.objects.get(username=self.user_data['username']))

    def test_can_create_account_with_first_name(self):
        """Tests that we can create an account with a first_name."""
        self.user_data['first_name'] = 'TestName'
        response = self.register()
        testUser = BasicUser.objects.get(username=self.user_data['username'])

        self.assertTrue(testUser)
        self.assertEqual(
            response.data['user']['first_name'], self.user_data['first_name'])

    def test_can_create_account_with_email(self):
        """Tests that we can create an account with a email."""
        self.user_data['email'] = 'test@test.test'
        response = self.register()
        testUser = BasicUser.objects.get(username=self.user_data['username'])

        self.assertTrue(testUser)
        self.assertEqual(
            response.data['user']['email'], self.user_data['email'])

    def test_fails_missing_username(self):
        """Test missing username gets rejected.

        Tests that response data contains ErrorDetail for username if missing
        username.
        """
        self.user_data['username'] = None
        response = self.register()

        self.assertEqual(response.data['username'], self.BlankFieldError)

    def test_fails_missing_password(self):
        """Test missing password gets rejected.

        Tests that response data contains ErrorDetail for password if missing
        password.
        """
        self.user_data['password'] = None
        response = self.register()
        self.assertEqual(response.data['password'], self.BlankFieldError)
