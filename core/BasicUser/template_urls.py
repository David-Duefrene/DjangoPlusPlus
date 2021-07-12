"""URLs list for the basic user model using Django's template system."""
# Django imports
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView

# Django REST imports
from rest_framework.routers import DefaultRouter

# Project imports
from .views import ListBasicUser, BasicUserDetail, CreateBasicUser, \
    LoginUser, UpdateUserView, DeleteUserView

router = DefaultRouter()

urlpatterns = [
    # View Users
    path('list/', ListBasicUser.as_view(), name='template_user_list'),
    path('view/<pk>', BasicUserDetail.as_view(), name='template_view_user'),

    # Account creation and authentication
    path('create/', CreateBasicUser.as_view(), name='template_create_user'),
    path('login/', LoginUser.as_view(template_name='Login.html'),
         name='template_login'),
    path('logout/', LogoutView.as_view(template_name='Logout.html'),
         name='template_logout'),
    path('edit/', UpdateUserView.as_view(), name='template_edit_user'),
    path('delete/', DeleteUserView.as_view(), name='template_delete_user'),

    # change password urls
    path('change_password/', PasswordChangeView.as_view(),
         name='template_change_password'),
    path('change_password/done/', PasswordChangeDoneView.as_view(),
         name='template_change_password_done'),

    # Reset password
    path('reset_password/', PasswordResetView.as_view(
        template_name='password/password_reset_form.html'),
        name='template_password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(
        template_name='Password_Reset_Done.html'),
        name='template_password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='template_Password_Reset_Confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='template_password_reset_complete.html'),
        name='password_reset_complete'),
] + router.urls
