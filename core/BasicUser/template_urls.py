"""URLs list for the basic user model using Django's template system."""
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from .views import ListBasicUser, BasicUserDetail, CreateBasicUser, \
    LoginUser, UpdateUserView

router = DefaultRouter()

urlpatterns = [
    path('createuser/', CreateBasicUser.as_view(),
         name='template_create_user'),
    path('userlist/', ListBasicUser.as_view(), name='template_user_list'),
    path('userdetail/<pk>', BasicUserDetail.as_view(),
         name='template_user_detail'),
    path('login/', LoginUser.as_view(template_name='Login.html'),
         name='template_login'),
    path('logout/', LogoutView.as_view(template_name='Logout.html'),
         name='template_logout'),
    path('edit/<pk>', UpdateUserView.as_view(), name='template_edit_user'),
] + router.urls
