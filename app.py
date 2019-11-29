from flask import Flask, request, redirect, jsonify
from flask import render_template, abort

app = Flask(__name__, template_folder='templates')


@app.route('/submit', methods=['GET', 'POST'])
def submit_info():
    if request.method == 'GET':
        abort(404)
    data = request.json
    print(data)
    return {'status': 'succeed'}


@app.route('/')
def index():
    infos = [Info(), Info()]
    return render_template('index.html', infos=infos)
