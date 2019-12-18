import json
from typing import List


class JEncoder(json.JSONEncoder):
    def default(self, o):
        att = [k for k in o.__dict__.keys() if not k.startswith('_')]
        att2val = {a: getattr(o, a) for a in att}
        att2val = {k: v for k, v in att2val.items() if not callable(v)}
        return att2val


class BaseObject(object):
    def __str__(self) -> str:
        return '{}: {}'.format(self.__class__.__name__, json.dumps(self, cls=JEncoder))

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self


class Link(BaseObject):
    def __init__(self, name=None, ips: List[str] = None, mac=None) -> None:
        super().__init__()
        self.name = name
        self.ips = ips
        self.mac = mac


class Device(BaseObject):
    _TABLE_KEY = 'name'

    def __init__(self, name=None, links: List[Link] = None, last_time=None) -> None:
        super().__init__()
        self.name = name
        self.links = links
        self.last_time = last_time


if __name__ == '__main__':
    devices = Device(links=[Link(), Link()])
    print('{}'.format(devices))
