"""device_storage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from devices.views import create_user, create_device, add_user_to_device, device_list, users_list, check_rfid

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/', create_user),
    path('create_device/', create_device),
    path('users/', users_list, name='users_list'),
    path('check_rfid/', check_rfid, name='check_rfid'),
    path('devices/', device_list, name='device_list'),
    path('add_user_to_device/', add_user_to_device, name='add_user_to_device'),


]
