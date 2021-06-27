"""Test the update user template."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from TestUtil.create_user import create_user


class UpdateUserTest(TestCase):
    """Test the Update User template view."""

    def setUp(self):
        """Set up a user in the test DB."""
        self.user = create_user(model=get_user_model())

    def test_update_anon_user_gets_redirected(self):
        """Test the Update User template view only allow auth users.

        Ensure the update basic user URL returns HTTP 302 if user is anon.
        """
        response = self.client.get("/template/BasicUser/edit/")
        self.assertEqual(response.status_code, 302)

    def test_update_user_page_url(self):
        """Test the Update User template view.

        Ensure the update basic user URL returns HTTP 200 and uses the correct template.
        """
        self.client.force_login(self.user)
        response = self.client.get("/template/BasicUser/edit/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='EditBasicUser.html')

    def test_update_user_page_view_name(self):
        """Test the Update User template view name.

        Ensure the update basic user view name returns HTTP 200 and uses the correct template.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('template_edit_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='EditBasicUser.html')

    def test_update_user_form(self):
        """Test the update user form."""
        self.client.force_login(self.user)
        updated_data = {
            'email': 'asd@asd.com', 'first_name': 'fName', 'last_name': 'lName'
        }
        response = self.client.post(reverse('template_edit_user'), data=updated_data)
        updated_user = get_user_model().objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.email, updated_data['email'])
        self.assertEqual(updated_user.first_name, updated_data['first_name'])
        self.assertEqual(updated_user.last_name, updated_data['last_name'])

    def test_update_user_template(self):
        """Test the update user template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('template_edit_user'))
        html = response.content.decode('utf8')

        # check header
        self.assertIn('<h2>Edits an Authenticated User</h2>', html)

        # check it has a csrf token
        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken" value=', html)

        # check has correct input labels
        self.assertIn('<label for="id_first_name">First name:</label>', html)
        self.assertIn('<label for="id_last_name">Last name:</label>', html)
        self.assertIn('<label for="id_email">Email:</label>', html)

        # check has correct inputs
        self.assertIn(f'<input type="text" name="first_name" value="{self.user.first_name}" maxlength="150" id="id_first_name">', html)
        self.assertIn(f'<input type="text" name="last_name" value="{self.user.last_name}" maxlength="150" id="id_last_name">', html)
        self.assertIn(f'<input type="email" name="email" value="{self.user.email}" maxlength="254" id="id_email">', html)

        # check button
        self.assertIn('<button type="submit">Edit User</button>', html)
