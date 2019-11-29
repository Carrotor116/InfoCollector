import signal
import sys

import gevent
from gevent.pywsgi import WSGIServer

import config
import network_util
from app import app as application


def _quit():
    print('Bye')
    sys.exit(0)


def run_server():
    # init conf
    # try:
    #     CmdOption().init_conf(sys.argv[1:])
    # except OptionError as e:
    #     print('ERROR: {}\n\n{}\n'.format(e.msg, usage_short))
    #     sys.exit(-1)

    print('InfoCollector is available at following address:')
    ips = network_util.get_ip_v4()
    for _ip in ips:
        print('  http://%s:%s' % (_ip, config.BIND_PORT))

    gevent.signal(signal.SIGINT, _quit)
    gevent.signal(signal.SIGTERM, _quit)
    http_server = WSGIServer(('0.0.0.0', int(config.BIND_PORT)), application)
    try:
        http_server.serve_forever()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_server()
