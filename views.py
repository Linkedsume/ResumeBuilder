from flask import Flask, redirect, url_for, session, request


app = Flask(__name__)
@app.route('/')
def index():
    return 'test'
