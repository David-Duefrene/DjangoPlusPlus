"""Views using Django templates to be used to show the Basic User model."""
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
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
    """Logs a user in."""

    success_url = reverse_lazy('template_list_all_users')

    def get_success_url(self):
        """Return success URL."""
        return self.success_url


class UpdateUserView(UpdateView):
    """Update the user."""

    model = BasicUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'EditBasicUser.html'
    success_url = 'template_user_detail'

    def get_success_url(self):
        """Get the URL for the user."""
        return(reverse(self.success_url, args=(self.object.id,)))
