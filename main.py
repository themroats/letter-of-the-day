from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
# from flask_sqlalchemy import SQLAlchemy


import random
import string
import logging
import json
import httplib2
import requests
import datetime
import time
import requests 

app = Flask(__name__)

from initdb import get_all_users, get_current_letter, set_next_letter, get_all_letters


@app.route("/")
def index():
    return render_template("letter.html", letter=get_current_letter().letter)

@app.route("/prev")
def show_previous_letters():
    return str(get_all_letters())

@app.route("/Implinks")
def showMain():
    a = "https://flask.palletsprojects.com/en/1.1.x/quickstart/"
    b = "https://github.com/pallets/flask"
    c = "https://medium.com/bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c"
    d = str(get_all_users())
    links = [a, b, c, d]
    return render_template("Implinks.html", links=links)

@app.route("/api/new_letter")
def new_letter():
    if request.headers.get("X-Appengine-Cron"):
        generate_next_letter()
        return "success", 200
    else:
        return "forbidden", 403


def generate_next_letter():
    previous_letter = get_current_letter().letter
    next_letter = previous_letter

    while next_letter == previous_letter:
        r = requests.get("https://www.random.org/integers/?num=1&min=0&max=25&col=1&base=10&format=plain&rnd=new")
        next_letter = chr(r.json() + 65)

    set_next_letter(next_letter)



if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", use_reloader=False)