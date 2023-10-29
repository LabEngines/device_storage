# serializers.py

from rest_framework import serializers
from .models import User, Device


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'slack_name', 'rfid_hash')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'device_name', 'device_mac')


class DeviceListSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ('id', 'device_name', 'device_mac', 'user')

    def get_user(self, obj):
        user_serializer = UserSerializer(obj.user)

        return user_serializer.data['slack_name']


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'slack_name', 'rfid_hash')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'slack_name', 'rfid_hash')