"""Model describing a Basic User for Django REST and templates."""
from django.db import models
from django.urls import reverse
from django.conf import settings

from decimal import InvalidOperation

from .abstract_model import AbstractBasicUser


class BasicUser(AbstractBasicUser, models.Model):
    """Basic User is a bare bones basic user.

    Basic User wraps Abstract Base User allowing testing as well as views.

    Methods:
        get_absolute_url: gets the url for api view user
    """

    @property
    def get_absolute_url(self):
        """Return the edit profile url."""
        try:
            if settings.RESPONSE_MODE == 'API':
                return reverse('api_view_user', kwargs={'pk': self.id})
            if settings.RESPONSE_MODE == 'TEMPLATE':
                return reverse('template_view_user', kwargs={'pk': self.id})

            raise InvalidOperation('Invalid Response Mode')

        except InvalidOperation:
            print('\033[91m ERROR: INVALID RESPONSE_MODE SET IN YOUR SETTING.PY\033[0m')  # noqa: E501
        except NameError:
            print('\033[91m ERROR: RESPONSE_MODE NOT SET IN YOUR SETTING.PY\033[0m')  # noqa: E501
