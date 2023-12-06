import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Device
from .serializers import UserSerializer, DeviceSerializer, DeviceListSerializer, UsersListSerializer

from functools import wraps

logger = logging.getLogger('django')


def logger_function(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        url = request.build_absolute_uri()
        logger.info(f"Endpoint called: {func.__name__}")
        logger.info(f"URL: {url}")
        if request.method == 'POST':
            request_body = json.loads(request.body)
            logger.info(f"Request Body: {request_body}")
        response = func(request, *args, **kwargs)
        response.render()
        logger.info(f"Response: {response.content.decode('utf-8')}")
        return response
    return wrapper


@logger_function
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@logger_function
@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@logger_function
@api_view(['GET'])
def device_list(request):
    devices = Device.objects.all()
    serializer = DeviceListSerializer(devices, many=True)

    return Response(serializer.data)


@logger_function
@api_view(['GET'])
def users_list(request):
    devices = User.objects.all()
    serializer = UsersListSerializer(devices, many=True)
    return Response(serializer.data)


@logger_function
@api_view(['GET'])
def check_rfid(request):
    rfid_hash = request.GET.get('rfid_hash')
    try:
        user = User.objects.get(rfid_hash=rfid_hash)
    except User.DoesNotExist:
        return JsonResponse({'error': f'User with RFID hash {rfid_hash} not found'}, status=400)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@logger_function
@csrf_exempt
def add_user_to_device(request):
    # Parse the request body as JSON

    body = json.loads(request.body)
    rfid_hash = body.get('rfid_hash')
    device_mac = body.get('device_mac')

    # Find the User object with the specified RFID hash
    try:
        user = User.objects.get(rfid_hash=rfid_hash)
    except User.DoesNotExist:
        return JsonResponse({'error': f'User with RFID hash {rfid_hash} not found'}, status=400)

    # Find the Device object with the specified MAC address
    try:
        device = Device.objects.get(device_mac=device_mac)
    except Device.DoesNotExist:
        return JsonResponse({'error': f'Device with MAC address {device_mac} not found'}, status=400)

        # Associate the user with the device
    if request.method == 'POST':
        device.user = user

    if request.method == 'DELETE':
        device.user = None

    device.save()

    return JsonResponse({'success': True})
