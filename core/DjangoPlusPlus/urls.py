"""DjangoPlusPlus URL Configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('api/BasicUser/', include('BasicUser.urls')),
    path('template/BasicUser/', include('BasicUser.template_urls')),
]
