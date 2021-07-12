"""Test the template Login view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from TestUtil.create_user import create_user


class LoginTest(TestCase):
    """Test the Login template view."""

    def test_login_page_url(self):
        """Test the LoginUser template view via URL.

        Ensure the LoginUser URL returns HTTP 200 and uses the correct template.
        """
        response = self.client.get("/template/BasicUser/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='Login.html')

    def test_login_page_view_name(self):
        """Test the LoginUser template view name.

        Ensure the LoginUser vier name returns HTTP 200 and uses the correct template.
        """
        response = self.client.get(reverse('template_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='Login.html')

    def test_login_form(self):
        """Test the login form"""
        user = create_user(model=get_user_model())
        response = self.client.post("/template/BasicUser/login/", data={
            'username': user.username, 'password': 'password',})

        self.assertEqual(response.status_code, 302)


    def test_login_page_template(self):
        """Test the LoginUser template."""
        response = self.client.get(reverse('template_login'))
        html = response.content.decode('utf8')

        self.assertIn('<h2>Log In</h2>', html)
        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken" value=', html)

        # test labels
        self.assertIn('<label for="id_username">Username:</label>', html)
        self.assertIn('<label for="id_password">Password:</label>', html)

        # test inputs
        self.assertIn('<input type="text" name="username" autofocus autocapitalize="none" autocomplete="username" maxlength="150" required id="id_username">', html)
        self.assertIn('<input type="password" name="password" autocomplete="current-password" required id="id_password">', html)
