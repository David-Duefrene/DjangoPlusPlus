"""Test the register template view."""
# from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class BaseUserRegisterTest(TestCase):
    """Test the register template view.

    Attributes:
        user_data: the data used to register a user.
    """

    def setUp(self):
        """Set up the user data."""
        self.user_data = {
            'username': 'test', 'email': 'asd@asd.com',
            'password': 'nrf6V2', 'first_name': ''
        }

    def test_register_page_url(self):
        """Test the CreateBasicUser template view.

        Ensure the create basic user URL returns HTTP 200 and uses the
        correct template.
        """
        response = self.client.get("/template/BasicUser/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='CreateBasicUser.html')

    def test_register_page_view_name(self):
        """Test the CreateBasicUser template view name.

        Ensure the CreateBasicUser view name return HTTP 200 and uses the
        correct template.
        """
        response = self.client.get(reverse('template_create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='CreateBasicUser.html')

    def test_register_form(self):
        """Test the registration."""
        response = self.client.post("/template/BasicUser/create/", data={
            'username': 'test', 'email': 'asd@asd.com',
            'password1': 'nrf6V2111', 'password2': 'nrf6V2111',
            'first_name': '', 'last_name': ''
        })

        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_template(self):
        """Test the registration template."""
        response = self.client.get(reverse('template_create_user'))
        html = response.content.decode('utf8')

        # check header
        self.assertIn('<h2>Create a User</h2>', html)

        # check it has a csrf token
        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken" value=', html)

        # check has correct input labels
        self.assertIn('<label for="id_username">Username:</label>', html)
        self.assertIn('<label for="id_email">Email:</label>', html)
        self.assertIn('<label for="id_first_name">First name:</label>', html)
        self.assertIn('<label for="id_last_name">Last name:</label>', html)
        self.assertIn('<label for="id_password1">Password:</label>', html)
        self.assertIn('<label for="id_password2">Password confirmation:</label>', html)

        # check has correct inputs
        self.assertIn('<input type="text" name="username" maxlength="150" autofocus required id="id_username">', html)
        self.assertIn('<input type="email" name="email" maxlength="254" id="id_email">', html)
        self.assertIn('<input type="text" name="first_name" maxlength="150" id="id_first_name">', html)
        self.assertIn('<input type="text" name="last_name" maxlength="150" id="id_last_name">', html)
        self.assertIn('<input type="password" name="password1" autocomplete="new-password" required id="id_password1">', html)
        self.assertIn('<input type="password" name="password2" autocomplete="new-password" required id="id_password2">', html)
