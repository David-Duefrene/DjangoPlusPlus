"""Tests the basic user model."""
import datetime

from django.test import TestCase

from BasicUser.models import BasicUser


class BasicUserModelTest(TestCase):
    """Tests the basic user model.

    Attributes:
        user: The test user.

    Methods:
        setUp: Sets up the user.

    Tests:
        testItHasInformationFields
        testItHasCreatedAndID
        testNameBlankStringReturnUsername
        testGetAbsoluteURLReturnsEditAccount
    """

    def setUp(self):
        """Create a basic user."""
        self.user = BasicUser.objects.create_user(
            username='BasicUser', password='nrf6V2',
            email='BasicUser@test.test', first_name='fName', last_name='lName')

    # Testing Model Fields
    def testItHasInformationFields(self):
        """Test that model has correct fields."""
        self.assertIsInstance(self.user.email, str)

    def testItHasCreatedAndID(self):
        """Test that the model has been created."""
        self.assertIsInstance(self.user.created, datetime.datetime)
        self.assertIsInstance(self.user.id, int)

    # Testing __str__ method
    def testNameBlankStringReturnUsername(self):
        """Test the __str__ method works as expected.

        Test that the username is returned when basic user is converted to a
        string if the user did not provide a name, and let it return the full
        name if provided.
        """
        self.assertEqual(str(self.user), 'fName lName')
        self.user.first_name = ''
        self.user.last_name = ''
        self.assertEqual(str(self.user), 'BasicUser')

    # Test the get_absolute_url method
    def testGetAbsoluteURLReturnsEditAccount(self):
        """Test the get_absolute_url method returns a string."""
        self.assertIsInstance(self.user.get_absolute_url, str)
