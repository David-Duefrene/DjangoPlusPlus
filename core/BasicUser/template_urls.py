"""URLs list for the basic user model using Django's template system."""
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from .views import ListBasicUser, BasicUserDetail, CreateBasicUser, LoginUser

router = DefaultRouter()

urlpatterns = [
    path('createuser/', CreateBasicUser.as_view(),
         name='template_create_user'),
    path('userlist/', ListBasicUser.as_view(), name='template_list_all_users'),
    path('userdetail/<pk>', BasicUserDetail.as_view(),
         name='template_user_detail'),
    path('login/', LoginUser.as_view(template_name='Login.html'),
         name='template_login'),
    path('logout/', LogoutView.as_view(template_name='Logout.html'),
         name='template_logout'),
] + router.urls
