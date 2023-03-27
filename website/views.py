from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import time
import uuid
import sqlite3

time_between_pairs = 20
time_for_each_pair = 5
session_id = str(uuid.uuid4())
views = Blueprint('views', __name__)


conn = sqlite3.connect(
    "/home/satarw/Documents/webapp/img_db", check_same_thread=False)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/select')
@login_required
def select():
    # select two random images from the database
    cur = conn.cursor()
    cur.execute("SELECT img_id, link FROM images ORDER BY RANDOM() LIMIT 2")
    rows = cur.fetchall()
    img1 = rows[0]
    img2 = rows[1]
    # render the select page with the two images
    return render_template('survey.html', img1=img1, img2=img2, user=current_user)


@views.route('/submit', methods=['POST'])
@login_required
def submit():
    # get the user's selection and the two images that were shown
    user_id = request.form['user_id']
    selection = request.form['selection']
    img1 = request.form['img1']
    img2 = request.form['img2']
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO data (user_id, session_id, img1, img2, selection) VALUES (?, ?, ?, ?, ?)",
                (user_id, session_id, img1, img2, selection))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect(url_for('views.select'))
