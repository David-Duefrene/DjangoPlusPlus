"""URLs list for the basic user module."""
# Django imports
from django.urls import path, include

# Django REST imports
from rest_framework.routers import DefaultRouter

# Knox imports
from knox.views import LogoutView

# Project imports
from .api import UserAPI, LoginAPI, ChangePasswordAPI, ListUsersAPI, \
    PasswordResetAPI, PasswordResetConfirmAPI

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('knox.urls')),

    # View users
    path('list/', ListUsersAPI.as_view(), name='api_user_list'),
    path('view/<pk>', UserAPI.as_view(), name='api_view_user'),

    # Create, change and auth users
    path('create/', UserAPI.as_view(), name='api_create_user'),
    path('login/', LoginAPI, name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('edit/', UserAPI.as_view(), name='api_edit_user'),
    path('delete/', UserAPI.as_view(), name='api_delete_user'),

    # Passwords
    path('change_password/', ChangePasswordAPI, name='api_change_password'),
    path('reset_password/', PasswordResetAPI.as_view(), name='api_reset_password'),  # noqa E501
    path('reset_password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmAPI.as_view(), name='password_reset_confirm'),
] + router.urls
