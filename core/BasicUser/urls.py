"""URLs list for the basic user module."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from knox.views import LogoutView

from .api import UserAPI, LoginAPI, ChangePasswordAPI

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('knox.urls')),
    path('create/', UserAPI.as_view(), name='basic_create_account'),
    path('login/', LoginAPI, name='basic_login'),
    path('logout/', LogoutView.as_view(), name='basic_logout_API'),
    path('edit/', UserAPI.as_view(), name='basic_edit_account'),
    path('change_password/', ChangePasswordAPI, name='basic_change_password'),
    path('reset_password/', include('django_rest_passwordreset.urls',
         namespace='basic_reset_password')),
] + router.urls
