import argparse
import logging
import os
import signal
import sys
import network_util
import gevent
from gevent.pywsgi import WSGIServer

from fserver import conf

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

    print('fserver is available at following address:')
    if conf.BIND_IP == '0.0.0.0':
        ips = network_util.get_ip_v4()
        for _ip in ips:
            print('  http://%s:%s' % (_ip, conf.BIND_PORT))
    else:
        print('  http://%s:%s' % (conf.BIND_IP, conf.BIND_PORT))

    gevent.signal(signal.SIGINT, _quit)
    gevent.signal(signal.SIGTERM, _quit)
    http_server = WSGIServer((conf.BIND_IP, int(conf.BIND_PORT)), application)
    try:
        http_server.serve_forever()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_server()
