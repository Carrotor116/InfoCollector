from flask import Flask, request, jsonify
from flask import render_template, abort

import db
from auth import auth_devices
from bean import Device, Link

app = Flask(__name__, template_folder='templates')
db.create_table(Device)


def response_failed(msg=None):
    return jsonify({'status': 'failed', 'msg': msg})


def response_succeed():
    return jsonify({'status': 'succeed'})


@app.route('/submit', methods=['GET', 'POST'])
def submit_devices():
    if request.method == 'GET':
        abort(404)

    data = request.json
    if data is None:
        return response_failed('Only support json data')

    try:
        device = Device(**data)
        device.links = [Link().update(**l) for l in data['links']]
        assert auth_devices(device)
    except Exception:
        print('invalid data: {}'.format(data))
        return response_failed('Invalid Device')
    dev = db.select_by_key(Device, device.name)
    if dev is None:
        if not db.insert(device):
            return response_failed('Database error')
    elif not db.update(device):
        return response_failed('Database error')

    return response_succeed()


@app.route('/')
def index():
    devices = db.select_all(Device)
    devices.sort(key=lambda d: d.name)
    for d in devices:
        d.links.sort(key=lambda l: l['mac'])
        for link in d.links:
            link['ips'].sort()
    return render_template('index.html', devices=devices)
