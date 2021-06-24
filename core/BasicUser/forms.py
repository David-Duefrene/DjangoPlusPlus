"""Contains forms for creating and editing a basic user."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model, password_validation
from django.forms import Form, CharField


class CreateBasicUserForm(UserCreationForm):
    """Form to create a basic user.

    Meta:
        model: The user model set in settings.py
        fields: A list of fields the user needs to create an account
    """

    class Meta:
        """The Meta

        Attributes:
            model: The user model set in settings.py
            fields: A list of fields the user needs to create an account
        """

        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2')


class EditBasicUserForm(UserChangeForm):
    """Form to edit a basic user.

    Meta:
        model: The user model set in settings.py
        fields: A list of fields the user can edit by default
    """

    class Meta:
        """The Meta

        Attributes:
            model: The user model set in settings.py
            fields: A list of fields the user can edit by default
        """

        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class SetBasicUserPassword(Form):
    """Set a new password if the user has reset it.

    Attributes:
        new_password: the password the user is changing to

    Methods:
        __init__(self, user): sets the user
        clean_new_password: validates the password
        save(commit-true): saves the new password to the database

    """

    new_password = CharField()

    def __init__(self, user, *args, **kwargs):
        """Set the user."""
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password(self):
        """Validate the password."""
        password = self.cleaned_data.get('new_password')
        password_validation.validate_password(password, self.user)
        return password

    def save(self, commit=True):
        """Save the password to the database."""
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
