"""Test the register template view."""
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
