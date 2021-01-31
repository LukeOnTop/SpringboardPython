# Put your app in here
from operations import *
from flask import Flask, request
app = Flask(__name__)


@app.route('/add')
def addition():
    a = request.args['a']
    a = int(a)
    b = request.args['b']
    b = int(b)
    return f"{add(a, b)}"


@app.route('/sub')
def subtract():
    a = request.args['a']
    a = int(a)
    b = request.args['b']
    b = int(b)
    return f"{sub(a, b)}"


@app.route('/mult')
def multiply():
    a = request.args['a']
    a = int(a)
    b = request.args['b']
    b = int(b)
    return f"{mult(a, b)}"


@app.route('/div')
def divide():
    a = request.args['a']
    a = int(a)
    b = request.args['b']
    b = int(b)
    c = div(a, b)
    c = int(c)
    return f"{c}"
