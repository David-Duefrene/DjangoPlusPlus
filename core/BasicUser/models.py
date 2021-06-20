"""Model describing a Basic User for Django REST and templates."""
from django.db import models

from AbstractModels.AbstractBaseUser.models import AbstractBasicUser


class BasicUser(AbstractBasicUser, models.Model):
    """Basic User is a bare bones basic user.

    Basic User wraps Abstract Base User allowing testing as well as views.
    Class is passed.
    """

    pass
