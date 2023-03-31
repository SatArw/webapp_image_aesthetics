from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import time
import uuid
import sqlite3
import random
import string

time_between_pairs = 20
time_for_each_pair = 5
views = Blueprint('views', __name__)

conn = sqlite3.connect(
    "/home/satarw/Documents/webapp/img_db", check_same_thread=False)

cur = conn.cursor()
cur.execute('SELECT * FROM IMAGES')
imgs = cur.fetchall()
total_imgs = len(imgs)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global sess_idntfr
    sess_idntfr = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=10))
    return render_template("home.html", user=current_user, sid=sess_idntfr)


@views.route('/select')
@login_required
def select():
    sess = sess_idntfr  # store the value of session_identifier from home
    cursorObject = conn.cursor()
    cursorObject.execute(
        "SELECT img1, img2 FROM data WHERE session_id = '{}' ".format(sess))  # select images from the database with same session_id so that they can be removed.
    res = cursorObject.fetchall()

    # make a list of all such rows and delete them
    lis = list(range(1, total_imgs+1))
    for x in res:
        lis.remove(x[0])
        lis.remove(x[1])

    # if all images are done, render the home page
    if len(lis) == 0:
        print("Done")
        return render_template('home.html', user=current_user)

    # make random choices and select those images
    i1 = random.choice(lis)
    lis.remove(i1)
    i2 = random.choice(lis)
    cursorObject.execute(
        "SELECT img_id,link FROM images WHERE img_id={}".format(i1))
    image1 = cursorObject.fetchone()
    cursorObject.execute(
        "SELECT img_id,link FROM images WHERE img_id={}".format(i2))
    image2 = cursorObject.fetchone()
    return render_template('survey.html', img1=image1, img2=image2, user=current_user)


@ views.route('/submit', methods=['POST'])
@ login_required
def submit():
    # get the user's selection and the two images that were shown
    user_id = request.form['user_id']
    selection = request.form['selection']
    img1 = request.form['img1']
    img2 = request.form['img2']
    sess_id = request.form['sess_id']
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO data (user_id, session_id, img1, img2, selection) VALUES (?, ?, ?, ?, ?)",
                (user_id, sess_idntfr, img1, img2, selection))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect(url_for('views.select'))
