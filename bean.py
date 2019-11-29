class Info(object):
    _TABLE_KEY = 'alias'

    def __init__(self, alias=None, ip=None, last_time=None, mac=None) -> None:
        super().__init__()
        self.alias = alias
        self.ip = ip
        self.last_time = last_time
        self.mac = mac

    def __str__(self):
        res = 'alias: {}, ip: {}, last_time: {}'.format(self.alias, self.ip, self.last_time)
        return res

    def update(self, data: dict):
        ignores = [self.update.__name__]
        attr = [i for i in self.__dict__.keys() if i not in ignores]
        for k, v in data.items():
            if k in attr:
                setattr(self, k, v)


if __name__ == '__main__':
    print(Info.__dict__)
    print(hasattr(Info, '_TABLE_KEY'))
