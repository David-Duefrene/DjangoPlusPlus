"""Test the login API."""
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser


class LoginAPITest(APITestCase):
    """Tests the Login API.

    Attributes:
        login_data: the data used to login with.
        BlankFieldError: The error that will be received if a required field
            is blank.
        IncorrectCredentialsError: The error that will be received if the
            username or password is incorrect.

    Methods:
        setUp(self): creates a user for every test.
        login(self): logs the user in with self.login_data.

    Tests:
        test_valid_credentials_can_login
        test_bad_username_is_rejected
        test_bad_password_is_rejected
        test_no_username_is_rejected
        test_no_password_is_rejected
    """

    def setUp(self):
        """Create a user, sets up login data."""
        user = create_user(model=BasicUser)
        self.login_data = {'username': user.username, 'password': 'password'}
        self.BlankFieldError = [ErrorDetail(
            string='This field may not be blank.', code='blank')]
        self.IncorrectCredentialsError = [ErrorDetail(
            string='Incorrect Credentials', code='invalid')]

    def login(self):
        """Log the user in with self.login_data.

        Returns the server response.
        """
        return self.client.post(reverse('api_login'), self.login_data)

    def test_valid_credentials_can_login(self):
        """Test to make sure valid data can login.

        Tests to make sure good username and passord returns a HTTP 200 code,
        a user object, and a token.
        """
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['user'])
        self.assertTrue(response.data['token'])

    def test_bad_username_is_rejected(self):
        """Test to make sure a bad username is rejected."""
        self.login_data['username'] = 'bad'
        response = self.login()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'],
                         self.IncorrectCredentialsError)

    def test_bad_password_is_rejected(self):
        """Test to make sure a bad password is rejected."""
        self.login_data['password'] = 'bad'
        response = self.login()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'],
                         self.IncorrectCredentialsError)

    def test_no_username_is_rejected(self):
        """Test to make sure no username is rejected."""
        self.login_data['username'] = ''
        response = self.login()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'username': self.BlankFieldError})

    def test_no_password_is_rejected(self):
        """Test to make sure no password is rejected."""
        self.login_data['password'] = ''
        response = self.login()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': self.BlankFieldError})
