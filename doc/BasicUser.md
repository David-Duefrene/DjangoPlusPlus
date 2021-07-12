# Basic User

A basic user containing the ability to allow anyone to create, update, delete their own account and to view any user profile. Also contains login/logout, change password, and reset password ability.

## Example Template Usage

`urls.py`
```python
"""URLs list for the basic user model using Django's template system."""
# Django imports
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView

# Django REST imports
from rest_framework.routers import DefaultRouter

# D++ imports
from .views import ListBasicUser, BasicUserDetail, CreateBasicUser, \
    LoginUser, UpdateUserView, DeleteUserView

router = DefaultRouter()

urlpatterns = [
    # View Users
    path('list/', ListBasicUser.as_view(), name='user_list'),
    path('view/<pk>', BasicUserDetail.as_view(), name='view_user'),

    # Account creation and authentication
    path('create/', CreateBasicUser.as_view(), name='create_user'),
    path('login/', LoginUser.as_view(template_name='Login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='Logout.html'), name='logout'),
    path('edit/', UpdateUserView.as_view(), name='template_edit_user'),
    path('delete/', DeleteUserView.as_view(), name='template_delete_user'),

    # change password urls
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('change_password/done/', PasswordChangeDoneView.as_view(), name='change_password_done'),

    # Reset password
    path('reset_password/', PasswordResetView.as_view(
        template_name='password/password_reset_form.html'),
        name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(
        template_name='Password_Reset_Done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='template_Password_Reset_Confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='template_password_reset_complete.html'),
        name='password_reset_complete'),
] + router.urls
```


## Example API usage

`urls.py`
```python
"""URLs list for the basic user module using Django REST."""
# Django imports
from django.urls import path, include

# Django REST imports
from rest_framework.routers import DefaultRouter

# Knox imports
from knox.views import LogoutView

# D++ imports
from .api import UserAPI, LoginAPI, ChangePasswordAPI, ListUsersAPI, \
    PasswordResetAPI, PasswordResetConfirmAPI

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('knox.urls')),

    # View users
    path('list/', ListUsersAPI.as_view(), name='user_list'),
    path('view/<pk>', UserAPI.as_view(), name='view_user'),

    # Create, change and auth users
    path('create/', UserAPI.as_view(), name='create_user'),
    path('login/', LoginAPI, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', UserAPI.as_view(), name='edit_user'),
    path('delete/', UserAPI.as_view(), name='delete_user'),

    # Passwords
    path('change_password/', ChangePasswordAPI, name='change_password'),
    path('reset_password/', PasswordResetAPI.as_view(), name='reset_password'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmAPI.as_view(),
         name='password_reset_confirm'),
] + router.urls
```
