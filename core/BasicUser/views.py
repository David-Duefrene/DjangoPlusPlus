"""Views using Django templates to be used to show the Basic User model."""
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import BasicUser
from .forms import CreateBasicUserForm


class ListBasicUser(ListView):
    """List all basic users in the database."""

    model = BasicUser
    template_name = 'ListBasicUser.html'


class BasicUserDetail(DetailView):
    """Gives the details to an individual user."""

    context_object_name = 'BasicUserDetail'
    queryset = BasicUser.objects.all()
    template_name = 'BasicUserDetail.html'


class CreateBasicUser(CreateView):
    """Creates a basic user"""

    form_class = CreateBasicUserForm
    success_url = reverse_lazy('template_user_detail')
    template_name = "CreateBasicUser.html"
