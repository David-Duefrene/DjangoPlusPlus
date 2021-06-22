"""URLs list for the basic user model using Django's template system."""
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from rest_framework.routers import DefaultRouter

from .views import ListBasicUser, BasicUserDetail, CreateBasicUser, \
    LoginUser, UpdateUserView, DeleteUserView

router = DefaultRouter()

urlpatterns = [
    # View Users
    path('view/<pk>', BasicUserDetail.as_view(), name='template_user_detail'),
    path('list/', ListBasicUser.as_view(), name='template_user_list'),

    # Account creation and authentication
    path('create/', CreateBasicUser.as_view(), name='template_create_user'),
    path('login/', LoginUser.as_view(template_name='Login.html'),
         name='template_login'),
    path('logout/', LogoutView.as_view(template_name='Logout.html'),
         name='template_logout'),
    path('edit/', UpdateUserView.as_view(), name='template_edit_user'),
    path('delete/', DeleteUserView.as_view(), name='template_delete_user'),

    # Reset password
    path('password_reset/', PasswordResetView.as_view(
        template_name='password/password_reset_form.html'),
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='Password_Reset_Done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='Password_Reset_Confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
        name='password_reset_complete'),
] + router.urls
