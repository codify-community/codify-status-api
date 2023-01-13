from flask.wrappers import Response
from flask import make_response, jsonify

def res(data, status=200):
    return make_response(jsonify(data), status)