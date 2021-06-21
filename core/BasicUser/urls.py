"""URLs list for the basic user module."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from knox.views import LogoutView

from .api import UserAPI, LoginAPI, ChangePasswordAPI

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('knox.urls')),
    path('create/', UserAPI.as_view(), name='api_create_user'),
    path('view/<pk>', UserAPI.as_view(), name='api_view_user'),
    path('login/', LoginAPI, name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout_API'),
    path('edit/', UserAPI.as_view(), name='api_edit_account'),
    path('change_password/', ChangePasswordAPI, name='api_change_password'),
    path('reset_password/', include('django_rest_passwordreset.urls',
         namespace='api_reset_password')),
] + router.urls
