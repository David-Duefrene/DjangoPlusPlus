"""Test the delete user template."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from TestUtil.create_user import create_user


class DeleteUserTest(TestCase):
    """Test the delete user template view.

    Attributes:
        user: The test user

    Methods:
        setUp(self): Sets the test user
    """

    def setUp(self):
        """Set up a user in the test DB."""
        self.user = create_user(model=get_user_model())

    def test_delete_anon_user_gets_redirected(self):
        """Test the delete User template view only allow auth users.

        Ensure the delete basic user URL returns HTTP 302 if user is anon.
        """
        response = self.client.get("/template/BasicUser/delete/")
        self.assertEqual(response.status_code, 302)

    def test_delete_user_page_url(self):
        """Test the delete User template URL.

        Ensure the delete basic user URL returns HTTP 200 and uses correct template.
        """
        self.client.force_login(self.user)
        response = self.client.get("/template/BasicUser/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_user_page_view_name(self):
        """Test the delete User template view name.

        Ensure the delete basic user view name returns HTTP 200 and uses correct template.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('template_delete_user'))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_form(self):
        """Test the delete User form."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('template_delete_user'))
        self.assertEqual(response.status_code, 302)
        print(response.content.decode('utf8'))

    def test_delete_user_template(self):
        """Test the delete User template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('template_delete_user'))
        html = response.content.decode('utf8')

        # check header
        self.assertIn('<h2>Delete Account?</h2>', html)

        # check it has a csrf token
        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken" value=', html)

        # check paragraph
        self.assertIn('<p>Your account as well as their related objects will be deleted. Are you sure?</p>', html)

        # check button
        self.assertIn('<input type="submit" value="Confirm deletion" name="confirm_delete" />', html)
        self.assertIn('<input type="submit" value="Cancel" name="cancel"/>', html)
