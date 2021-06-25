"""Test to make sure a user can edit their profile."""
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser


class EditProfileAPITest(APITestCase):
    """Test the Edit Profile API.

    Attributes:
        client: The API client.
        updated_data(dict): Data we are going to update the profile with.
        user(TestBaseUser): The test user.
        response: The test servers response.

    Methods:
        setup(self): resets the class attribute back to defaults.
        update_user(self): updates the user with the given data.

    Tests:
        test_can_update_user_profile
        test_name_is_optional
        test_email_is_optional
    """

    def setUp(self):
        """Set up the client, update_data, user, and response."""
        self.client = APIClient()
        # Data we are going to update with
        self.updated_data = {
            'email': 'updateTest@test.com',
            'first_name': 'updatedFirstName',
            'last_name': 'updatedLastName',
        }
        self.user = create_user(model=BasicUser)
        self.response = None

    def update_user(self):
        """Update the user's profile.

        Updates the user's profile with updated_data and updates the user and
        adds the server response response.
        """
        self.client.force_authenticate(user=self.user)
        self.response = self.client.patch(
            reverse('api_edit_account'),
            self.updated_data)
        self.user = BasicUser.objects.get(username=self.user.username)

    def test_can_update_user_profile(self):
        """Test that we can update the user profile."""
        self.client.force_authenticate(user=self.user)
        self.update_user()
        self.assertEqual(self.user.first_name, self.updated_data['first_name'])
        self.assertEqual(self.user.last_name, self.updated_data['last_name'])
        self.assertEqual(self.user.email, self.updated_data['email'])

    def test_name_is_optional(self):
        """Test that the name fields is optional."""
        self.updated_data['first_name'] = ''
        self.updated_data['last_name'] = ''
        self.update_user()
        self.assertEqual(self.user.first_name, self.updated_data['first_name'])

    def test_email_is_optional(self):
        """Test that the email field is optional."""
        self.updated_data['email'] = ''
        self.update_user()
        self.assertEqual(self.user.email, self.updated_data['email'])
