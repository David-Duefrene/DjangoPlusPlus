"""Model describing a Basic User."""
from django.db.models import CharField
from django.db import models
from django.urls import reverse

from AbstractModels.AbstractBaseUser.models import AbstractBasicUser


class BasicUser(AbstractBasicUser, models.Model):
    """Basic User is a bare bones basic user.

    Basic User wraps Abstract Base User allowing testing as well as views.
    Only adds ability to return URL for the account.

    Attributes:
        URL_view_name: The view name get_absolute_url will lookup via reverse
            default is basic_edit_account.
    """

    URL_view_name = CharField(max_length=256, default='basic_edit_account')

    @property
    def get_absolute_url(self):
        """Return the edit profile url."""
        return reverse(self.URL_view_name)
