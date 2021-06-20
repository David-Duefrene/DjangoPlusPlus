"""Abstract models for an abstracted basic user account."""
from decimal import InvalidOperation
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import EmailField, DateTimeField, BigAutoField
from django.urls import reverse
from django.conf import settings


class AbstractBasicUser(AbstractUser):
    """AbstractBasicUser is an abstract model that describes a basic user.

    Attributes:
        objects: UserManager
        id(string): The unique ID for the user
        email(EmailField): The user's email, optional
        created(DateTimeField): The time the account was created

    Meta:
        ordering(list): Orders the users by id
        abstract(bool): Model is an abstract class

    Methods:
        __str__(self): Return name or username as a string
        get_absolute_url(self): Returns the users edit url
    """

    objects = UserManager()
    id = BigAutoField(primary_key=True)
    email = EmailField(blank=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        """The Meta.

        Attributes:
            ordering: id
            abstract(bool): True
        """

        ordering = ['-id']
        abstract = True

    def __str__(self):
        """Return the name or username as a string."""
        if self.get_full_name() == '':
            return self.username
        return f'{self.first_name} {self.last_name}'

    @property
    def get_absolute_url(self):
        """Return the edit profile url."""
        try:
            if settings.RESPONSE_MODE == 'API':
                return reverse('api_edit_account')
            raise InvalidOperation('Invalid Response Mode')

        except InvalidOperation:
            print('\033[91m ERROR: INVALID RESPONSE_MODE SET IN YOUR SETTING.PY\033[0m')  # noqa: E501
        except NameError:
            print('\033[91m ERROR: RESPONSE_MODE NOT SET IN YOUR SETTING.PY\033[0m')  # noqa: E501
