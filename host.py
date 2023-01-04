from flask import Flask, render_template, Blueprint, request, jsonify
import gevent.pywsgi

import sys
sys.dont_write_bytecode = True

app = Flask(__name__, template_folder='templates', static_folder='templates/images')
app.config['ghostboy.dev'] = 'ghostboy.dev:5000'
bp = Blueprint('image', __name__, subdomain="<user>")


@app.route('/', methods=['GET'])
def imgpage():
    return render_template('index.html'), 200


import endpoints.static.upload
app.add_url_rule('/upload', 'upload', endpoints.static.upload.uploader, methods=['POST', 'GET'])

import endpoints.static.imagerender
app.add_url_rule('/<imgfile>', 'sender', endpoints.static.imagerender.sender)


@app.route('/image', methods=['GET'])
def home():
    return render_template('invalid.html'), 400



#Key stuff
import endpoints.keymanagement.createkey
app.add_url_rule('/createkey', 'createkey', endpoints.keymanagement.createkey.createkey)

import endpoints.keymanagement.deletekey
app.add_url_rule('/deletekey', 'deletekey', endpoints.keymanagement.deletekey.deletekey)

import endpoints.keymanagement.config
app.add_url_rule('/config', 'config', endpoints.keymanagement.config.config)

import endpoints.keymanagement.fetchkeys
app.add_url_rule('/fetchkeys', 'fetchkeys', endpoints.keymanagement.fetchkeys.fetchkeys)

import endpoints.keymanagement.resetkey
app.add_url_rule('/reset', 'reset', endpoints.keymanagement.resetkey.reset)


@app.errorhandler(404)
def errorhandler(e):
    errorres = {
        "Error": "Endpoint not found"
    }
    return errorres, 404


from werkzeug.exceptions import HTTPException
import endpoints.methods
@app.errorhandler(Exception)
def handle_exception(e):
    errorres = {
        "Error": "Something went wrong"
    }
    if isinstance(e, HTTPException):
        return e

    connectip = request.headers.get('X-Forwarded-For').split(', ')[0]
    endpoints.methods.errrorpost(reqip=str(connectip), error=str(e))
    return jsonify(errorres), 500 

app.register_blueprint(bp)

app_server = gevent.pywsgi.WSGIServer(('localhost', 755), app)
app_server.serve_forever()
