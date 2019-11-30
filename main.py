import signal
import sys
import argparse
import gevent
from gevent.pywsgi import WSGIServer

import config
import network_util
from app import app as application


def _quit():
    print('Bye')
    sys.exit(0)


def run_server():
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=config.BIND_PORT,
                        help='port for listening, default [{}]'.format(config.BIND_PORT))
    parser.add_argument('--database', type=str, default=config.DATABASE,metavar='DB_NAME',
                        help='sqlite3 database name, default [{}]'.format(config.DATABASE))
    args = parser.parse_args()
    config.BIND_PORT = args.port
    config.DATABASE = args.database
    run_server()


if __name__ == '__main__':
    main()
