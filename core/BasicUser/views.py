"""Views using Django templates to be used to show the Basic User model."""
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .models import BasicUser
from .forms import CreateBasicUserForm


class CreateBasicUser(CreateView):
    """Creates a basic user"""

    form_class = CreateBasicUserForm
    success_url = reverse_lazy('template_user_list')
    template_name = "CreateBasicUser.html"


class ListBasicUser(ListView):
    """List all basic users in the database."""

    model = BasicUser
    template_name = 'ListBasicUser.html'


class BasicUserDetail(DetailView):
    """Gives the details to an individual user."""

    context_object_name = 'BasicUserDetail'
    queryset = BasicUser.objects.all()
    template_name = 'BasicUserDetail.html'


class LoginUser(LoginView):
    """Logs a user in.

    Required due to diffrent URL structure than default.
    """

    success_url = reverse_lazy('template_user_list')

    def get_success_url(self):
        """Return success URL."""
        return self.success_url


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """Update the user.

    Allows a user to update their own profile.

    Attributes:
        model: Set to BasicUser
        fields: only allows email, first and last names to be modified
        template_name: The template to be rendered, default EditBasicUser

    Methods:
        get_object: Make sure only the user can update their account
        get_success_url: Returns the user profile if successful
    """

    model = BasicUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'EditBasicUser.html'

    def get_object(self, queryset=None):
        """Ensure user can only update their own account."""
        return self.request.user

    def get_success_url(self):
        """Return the user profile URL."""
        return reverse_lazy('template_user_detail',
                            kwargs={'pk': self.request.user.id})


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """Delete the currently logged in user.

    Permits a user to delete their own account.

    Attributes:
        model: Set to BasicUser
        template_name: The template used to confirm deletion
        success_url: The URL to go to when successful
        login_url: The URL to go to if the user is not logged in

    Methods:
        get_object(self, queryset=None): Returns the currently logged in user
    """

    model = BasicUser
    template_name = 'DeleteUser.html'
    # TODO change to homepage after creating it
    success_url = reverse_lazy('template_user_list')
    login_url = reverse_lazy('template_login')

    def get_object(self, queryset=None):
        """Ensure user can only delete their own account."""
        return self.request.user
