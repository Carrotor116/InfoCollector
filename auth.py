import config
from bean import Device


def auth_devices(devices: Device):
    if devices.name is None or devices.ip is None:
        return False
    name = devices.name.upper()
    if name in config.DEVICE_MAC and \
            devices.mac not in config.DEVICE_MAC[name]:
        return False
    return True
