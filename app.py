from flask import Flask, request, jsonify
from flask import render_template, abort

import db
from auth import auth_devices
from bean import Device

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

    device = Device().update(data)
    if not auth_devices(device):
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
    return render_template('index.html', devices=devices)
