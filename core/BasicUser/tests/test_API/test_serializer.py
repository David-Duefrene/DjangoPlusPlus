"""Tests the Basic User serializers."""
from rest_framework.test import APITestCase

from TestUtil.create_user import create_user
from BasicUser.models import BasicUser
from BasicUser.serializers import BasicUserSerializer, RegisterSerializer, \
    LoginSerializer, ChangePasswordSerializer


class UserSerializerTest(APITestCase):
    """Tests the basic user serializer.

    Attributes:
        user: The test user.
        serializer: A BasicUserSerializer instance.

    Methods:
        setUp: Sets the test user and serializer.

    Tests:
        test_contains_expected_fields
    """

    def setUp(self):
        """Set up a user and serializer."""
        self.user = create_user(model=BasicUser)
        self.serializer = BasicUserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test the basic user serializer has expected fields.

        Test to make sure the basic user serializer only returns username,
        email, first_name, last_name, and the get_absolute_url.
        """
        self.assertEqual(
            set(self.serializer.data.keys()),
            set(['username', 'email', 'first_name', 'last_name',
                 'get_absolute_url']))


class RegisterSerializerTest(APITestCase):
    """Tests the register serializer.

    Attributes:
        user: The test user.
        serializer: A BasicUserSerializer instance.

    Methods:
        setUp: Sets the test user and serializer.

    Tests:
        test_contains_expected_fields
    """

    def setUp(self):
        """Set up a basic user and register serializer."""
        self.user = create_user(model=BasicUser)
        self.serializer = RegisterSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test the RegisterSerializer has expected fields.

        Test to make sure the RegisterSerializer returns only a username,
        email, and name.
        """
        self.assertEqual(
            set(self.serializer.data.keys()),
            set(['username', 'email', 'first_name', 'last_name']))


class LoginSerializerTest(APITestCase):
    """Tests the login serializer.

    Attributes:
        user: The test user.
        serializer: A BasicUserSerializer instance.

    Methods:
        setUp: Sets the test user and serializer.

    Tests:
        test_contains_expected_fields
    """

    def setUp(self):
        """Set up a user and login serializer."""
        self.user = create_user(model=BasicUser)
        self.serializer = LoginSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test the login serializer has expected fields.

        Test to make sure the login serializer takes only a username
        and password
        """
        self.assertEqual(set(self.serializer.data.keys()),
                         set(['username', 'password']))


class ChangePasswordSerializerTest(APITestCase):
    """Tests the change password serializer.

    Attributes:
        user: The test user.
        serializer: A BasicUserSerializer instance.

    Methods:
        setUp: Sets the test user and serializer.

    Tests:
        test_contains_expected_fields
    """

    def setUp(self):
        """Set up password data and change password serializer."""
        test = {'old_password': 'old', 'new_password': 'new'}
        self.serializer = ChangePasswordSerializer(instance=test)

    def test_contains_expected_fields(self):
        """Test the change password serializer has expected fields.

        Test to make sure the change password serializer only takes an old and
        new password.
        """
        self.assertEqual(set(self.serializer.data.keys()),
                         set(['old_password', 'new_password']))
