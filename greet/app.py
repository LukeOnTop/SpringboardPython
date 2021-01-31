from flask import Flask
app = Flask(__name__)


@app.route('/welcome')
def welcome():
    return "WELCOME!"


@app.route('/welcome/home')
def home():
    return "Welcome Home!"


@app.route('/welcome/back')
def back():
    return "Welcome Back!"
