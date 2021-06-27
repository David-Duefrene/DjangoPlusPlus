"""Test the list user's template view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from TestUtil.create_user import create_user


class ListUserTest(TestCase):
    """Test the register template view.

    Attributes:
        user_data: the data used to register a user.
    """

    def setUp(self):
        """Set up 50 users in the test DB."""
        for unused in range(30):
            create_user(model=get_user_model())

    def test_list_page_url(self):
        """Test the ListBasicUser template view via URL.

        Ensure the list basic user URL returns HTTP 200 and uses the
        correct template.
        """
        response = self.client.get("/template/BasicUser/list/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='ListBasicUser.html')

    def test_list_page_view_name(self):
        """Test the ListBasicUser view name.

        Ensure the ListBasicUser view name return HTTP 200 and uses the
        correct template.
        """
        response = self.client.get(reverse('template_user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='ListBasicUser.html')

    def test_pagination(self):
        """Test that pagination is set to 25 by default."""
        response = self.client.get(reverse('template_user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['user_list']), 25)

    def test_lists_all_users(self):
        """Test to ensure second page only has 5 user's."""
        response = self.client.get(reverse('template_user_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['user_list']), 5)
