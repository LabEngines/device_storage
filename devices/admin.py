from django.contrib import admin
from .models import User, Device


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('slack_name', 'rfid_hash')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_mac', 'user')
    list_filter = ('user',)
    search_fields = ('device_name', 'device_mac')
