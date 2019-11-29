import logging
import sys


class Color(object):
    GRAY = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    CRIMSON = 38


def colorize(string, color, bold=False, highlight=False):
    attr = []
    num = color
    if highlight:
        num += 10
    attr.append(str(num))
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


class MulLinesFormatter(logging.Formatter):
    def __init__(self, fmt=None, fmt_mid=None, fmt_last=None, datefmt=None):
        super(MulLinesFormatter, self).__init__(fmt, datefmt=datefmt)
        self._fmt_mid = fmt_mid if fmt_mid is not None else fmt
        self._fmt_last = fmt_last if fmt_last is not None else fmt

    def formatMessage(self, record):
        record_dics = []
        message = record.message
        record_dic = record.__dict__
        for i in message.split('\n'):
            tmp = dict(record_dic)
            tmp['message'] = i
            record_dics.append(tmp)

        res = []
        lines = len(record_dics)
        for ind, r in enumerate(record_dics):
            if ind == 0:
                res.append(self._fmt % r)
            elif ind == lines - 1:
                res.append(self._fmt_last % r)
            else:
                res.append(self._fmt_mid % r)

        return '\n'.join(res)


_logger = logging.getLogger('fserver')
_handler = logging.StreamHandler(sys.stdout)
_handler.setLevel(logging.DEBUG)
_formatter = MulLinesFormatter(fmt=colorize('[P%(process)d|T%(asctime)s @%(filename)s]', Color.GREEN) + ' %(message)s',
                               fmt_mid=colorize('[P%(process)d|T%(asctime)s @%(filename)s', Color.GREEN) +
                                       colorize(']', Color.GREEN, bold=True) + ' %(message)s',
                               fmt_last=colorize('[P%(process)d|T%(asctime)s @%(filename)s', Color.GREEN) +
                                        colorize(']', Color.GREEN, bold=True) + ' %(message)s',
                               datefmt='%Y.%m.%d_%H:%M:%S')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.DEBUG)
