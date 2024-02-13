from django.db import models


class User(models.Model):
    slack_name = models.CharField(max_length=100, unique=True)
    rfid_hash = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username


class Device(models.Model):
    device_name = models.CharField(max_length=100, unique=True)
    device_mac = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.device_name


class DeviceLog(models.Model):
    pass