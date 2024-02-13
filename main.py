import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import re
import subprocess
import time
import pyudev
import requests

from threading import Thread

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

last_rfid_hash = None
server_url = "http://192.168.0.6:81"
RELAY_PIN = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RELAY_PIN, GPIO.OUT)

devices = context.list_devices(subsystem='usb')


def get_devices():
    """
    Get all devices from DB

    :return: json
    """
    resp = requests.get(url=server_url + "/devices")

    return resp.json()


def is_device_exist(device_id):
    """
    Get all devices and check if device exist in DB

    :param device_id:
    :return:
    """

    devices = get_devices()

    for device in devices:
        if device['device_mac'] == device_id:
            return True
    return False


def device_monitor():
    """
    Check if device connected - remove user from device
    Check if device disconnected - add user to device
    :return:
    """
    global devices

    for device in iter(monitor.poll, None):
        vendor_id = device.get('ID_VENDOR_ID')
        model_id = device.get('ID_MODEL_ID')
        device_mac = f'{vendor_id}:{model_id}'
        if device.action == 'add':
            print("ADD")
            # do something very interesting here.
            print(device_mac)
            if vendor_id and model_id and is_device_exist(device_mac):
                json = \
                    {
                        'rfid_hash': last_rfid_hash,
                        'device_mac': str(device_mac)
                    }
                print("DEVICE rfid_hash and device_mac")

                # Fix me: REMOVE USER FROM DEVICE
                requests.delete(url=server_url + "/add_user_to_device/", json=json)
                devices = context.list_devices(subsystem='usb')

        if device.action == 'remove':
            print("REMOVE")
            devices = get_devices()
            connected_devices = get_connected_devices()

            # Находим все значения ключа 'device_mac' в первом списке, которые отсутствуют во втором списке
            devices_mac = set(dev['device_mac'] for dev in devices) - set(dev['id'] for dev in connected_devices)
            print(devices_mac)

            for device in devices_mac:
                json = \
                    {
                        'rfid_hash': last_rfid_hash,
                        'device_mac': device
                    }
                requests.post(url=server_url + "/add_user_to_device/", json=json)

        vendor_id = None
        model_id = None
        device_mac = None


def get_connected_devices():
    """
    Get connected devices by lsusb

    :return: list of dicts
    """
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    dev = df.decode('utf-8')
    print(dev)
    for i in dev.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    print(devices)

    return devices


def check_rfid_open_lock(rfid):
    """
    Check if rfid exists in DB and open lock
    :param rfid:
    :return:
    """
    global last_rfid_hash
    resp = requests.get(url=server_url + "/check_rfid", params={'rfid_hash': rfid})
    if resp.status_code == 200:
        last_rfid_hash = resp.json()['rfid_hash']
        open_lock()


def rfid_125khz_monitor():
    """
    Get rfid data for 125khz rfid

    :return:
    """

    with open('/dev/tty', 'r') as tty:
        while True:
            # cek apakah power ON
            rfid = tty.readline()
            time.sleep(0.5)

            if rfid:
                rfid = str(rfid)[:10]
                print('Hey your rfid is: {}'.format(rfid))
                check_rfid_open_lock(rfid)

            time.sleep(0.5)


def rfid_13mhz_monitor():
    """
    Get rfid data for 13mhz rfid

    :return:
    """
    global last_rfid_hash
    while True:
        reader = SimpleMFRC522()
        try:
            id, text = reader.read()
            time.sleep(0.5)
            print(id)
            print(text)
            check_rfid_open_lock(id)
        finally:
            GPIO.cleanup()
            time.sleep(0.5)


def open_lock():
    """Unlock the door lock and close after 3 seconds"""
    print("Opening door lock...")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(3)
    GPIO.output(RELAY_PIN, GPIO.HIGH)


rfid_125khz_monitor = Thread(target=rfid_125khz_monitor).start()
# rfid_13mhz_monitor = Thread(target=rfid_13mhz_monitor).start()
device_monitor = Thread(target=device_monitor).start()
