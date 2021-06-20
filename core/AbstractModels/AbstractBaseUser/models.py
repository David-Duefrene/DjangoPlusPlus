"""Abstract models for a basic user account."""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import EmailField, DateTimeField, BigAutoField, CharField
from django.urls import reverse


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
    URL_view_name = CharField(max_length=256, default='api_edit_account')

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
        return reverse(self.URL_view_name)
