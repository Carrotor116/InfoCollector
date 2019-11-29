import os
import requests
import argparse
import time


def get_links():
    lines = os.popen('ip link').read().split('\n')
    lines_link = [lines[i * 2] for i in range(int(len(lines) / 2))]
    lines_macs = [lines[i * 2 + 1] for i in range(int(len(lines) / 2))]
    links, macs = [], []
    for li in lines_link:
        link = li.strip().split(': ')[1]
        links.append(link)
    for li in lines_macs:
        mac = li.strip().split(' ')[1]
        macs.append(mac)
    return links, macs


def get_ipv4(link):
    lines = os.popen('ip -4 add show {}'.format(link)).read().split('\n')
    if len(lines) < 2:
        return []
    lines = lines[1:]
    lines = [lines[i * 2] for i in range(int(len(lines) / 2))]
    ips = []
    for li in lines:
        ip = li.strip().split(' ')[1].split('/')[0]
        ips.append(ip)
    return ips


def find_ip(ip_pattern):
    links, macs = get_links()
    ret = []
    for lk, mac in zip(links, macs):
        ips = get_ipv4(lk)
        for ip in ips:
            if ip_pattern in ip:
                ret.append((lk, mac, ip))
    return ret


def report_ip(service_ip, service_port, ip_pattern, device_name):
    ip_info = find_ip(ip_pattern)
    if len(ip_info) == 0:
        return
    assert len(ip_info) == 1, ip_info
    _, mac, ip = ip_info[0]

    t = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
    data = {'ip': ip, 'mac': mac, 'name': device_name, 'last_time': t}
    url = 'http://{}:{}/submit'.format(service_ip, service_port)
    ok = requests.post(url, json=data)
    return ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service_ip', required=True)
    parser.add_argument('--service_port', required=True, type=int)
    parser.add_argument('--device_name', required=True)
    parser.add_argument('--ip_pattern', default='172.17')
    args = parser.parse_args()
    ok = report_ip(args.service_ip, args.service_port, args.ip_pattern, args.device_name)
    print('succeed' if ok else 'failed')
