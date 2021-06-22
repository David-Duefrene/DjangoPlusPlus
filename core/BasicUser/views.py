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


class UpdateUserView(UpdateView):
    """Update the user."""

    model = BasicUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'EditBasicUser.html'
    success_url = reverse_lazy('template_user_detail')


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
