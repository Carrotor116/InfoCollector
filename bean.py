class Device(object):
    _TABLE_KEY = 'name'

    def __init__(self, name=None, ip=None, last_time=None, mac=None) -> None:
        super().__init__()
        self.name = name
        self.ip = ip
        self.last_time = last_time
        self.mac = mac

    def __str__(self):
        res = 'name: {}, ip: {}, last_time: {}'.format(self.name, self.ip, self.last_time)
        return res

    def update(self, data: dict):
        ignores = [self.update.__name__]
        attr = [i for i in self.__dict__.keys() if i not in ignores]
        for k, v in data.items():
            if k in attr:
                setattr(self, k, v)
        return self


if __name__ == '__main__':
    print(Device.__dict__)
    print(hasattr(Device, '_TABLE_KEY'))
