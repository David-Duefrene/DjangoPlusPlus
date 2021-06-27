"""Test the user's detail template view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from TestUtil.create_user import create_user


class ViewUserTest(TestCase):
    """Test the user's detail template view.

    Attributes:
        user: the user that should be displayed.
    """

    def setUp(self):
        """Set up a user in the test DB."""
        self.user = create_user(model=get_user_model())

    def test_detail_page_url(self):
        """Test the BasicUserDetail template view via URL.

        Ensure the BasicUserDetail URL returns HTTP 200 and uses the correct template.
        """
        response = self.client.get("/template/BasicUser/view/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='BasicUserDetail.html')

    def test_detail_page_view_name(self):
        """Test the BasicUserDetail view name.

        Ensure the BasicUserDetail view name return HTTP 200 and uses the
        correct template.
        """
        response = self.client.get(reverse('template_user_detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='BasicUserDetail.html')

    def test_detail_template(self):
        """Test the template renders the proper user attributes."""
        response = self.client.get(reverse('template_user_detail', kwargs={'pk': '1'}))
        html = response.content.decode('utf8')

        self.assertIn('<h2>User Details</h2>', html)
        self.assertIn(f'<li>Username: {self.user.username}</li>', html)
        self.assertIn(f'<li>First Name: {self.user.first_name}</li>', html)
        self.assertIn(f'<li>Last Name: {self.user.last_name}</li>', html)
        self.assertIn(f'<li>Email: {self.user.email}</li>', html)
        self.assertIn(f'<li>Profile URL: {self.user.get_absolute_url}</li>', html)
