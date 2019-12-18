import os
import requests
import argparse
import time


def get_link2mac():
    lines = os.popen('ip link').read().split('\n')
    lines_link = [lines[i * 2] for i in range(int(len(lines) / 2))]
    lines_macs = [lines[i * 2 + 1] for i in range(int(len(lines) / 2))]
    ret = dict()
    for ll, ml in zip(lines_link, lines_macs):
        link = ll.strip().split(': ')[1]
        mac = ml.strip().split(' ')[1]
        ret[link] = mac
    return ret


def get_ipv4(link):
    lines = os.popen('ip -4 add show {}'.format(link)).read().split('\n')
    if len(lines) < 2:
        return []
    lines = lines[1:]
    lines = [lines[i * 2] for i in range(int(len(lines) / 2))]
    ips = set()
    for li in lines:
        ip = li.strip().split(' ')[1].split('/')[0]
        ips.add(ip)
    ignore = ('127.0.0.1',)
    for i in ignore:
        if i in ips:
            ips.remove(i)
    ips = [i for i in ips if not i.startswith('169.254')]
    return ips


def get_links():
    link2mac = get_link2mac()
    links = []
    for link, mac in link2mac.items():
        ips = get_ipv4(link)
        links.append({'name': link,
                      'mac': mac,
                      'ips': ips})
    return links


def report_ip(service_ip, service_port, device_name):
    links = get_links()

    t = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
    data = {'name': device_name, 'links': links, 'last_time': t}
    url = 'http://{}:{}/submit'.format(service_ip, service_port)
    resp = requests.post(url, json=data).json()
    if resp is not None and 'status' in resp:
        return resp['status'] == 'succeed'
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service_ip', required=True)
    parser.add_argument('--service_port', required=True, type=int)
    parser.add_argument('--device_name', required=True)
    args = parser.parse_args()
    ok = report_ip(args.service_ip, args.service_port, args.device_name)
    print('succeed' if ok else 'failed')
