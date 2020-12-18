from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint


import random
import string
import logging
import json
import httplib2
import requests
import datetime
import time
import requests 


from initdb import get_all_users, get_current_letter, set_next_letter, get_all_letters
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template("letter.html", letter=get_current_letter().letter)

@main.route("/prev")
def show_previous_letters():
    return str(get_all_letters())

@main.route("/api/new_letter")
def new_letter():
    if request.headers.get("X-Appengine-Cron"):
        generate_next_letter()
        return "success", 200
    else:
        return "forbidden", 403

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

def generate_next_letter():
    previous_letter = get_current_letter().letter
    next_letter = previous_letter

    while next_letter == previous_letter:
        r = requests.get("https://www.random.org/integers/?num=1&min=0&max=25&col=1&base=10&format=plain&rnd=new")
        next_letter = chr(r.json() + 65)

    set_next_letter(next_letter)
