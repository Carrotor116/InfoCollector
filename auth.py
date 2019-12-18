import config
from bean import Device


def auth_devices(devices: Device):
    if devices.name is None or devices.links is None or len(devices.links) == 0:
        return False
    name = devices.name
    if name in config.DEVICE_MAC.keys():
        if all(link.mac not in config.DEVICE_MAC[name] for link in devices.links):
            return False
    return True
