"""URLs list for the basic user model using Django's template system."""
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ListBasicUser, BasicUserDetail, CreateBasicUser

router = DefaultRouter()

urlpatterns = [
    path('createuser/', CreateBasicUser.as_view(),
         name='template_create_user'),
    path('userlist/', ListBasicUser.as_view(), name='template_list_all_users'),
    path('userdetail/<pk>', BasicUserDetail.as_view(),
         name='template_user_detail'),
] + router.urls
