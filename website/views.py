from flask import Blueprint, render_template, request, redirect, url_for, session,flash
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
    "img_db", check_same_thread=False)

cur = conn.cursor()
cur.execute('SELECT * FROM images')
imgs = cur.fetchall()
total_imgs = len(imgs)

cur.execute('SELECT * FROM aspect_images')
imgs = cur.fetchall()
total_imgs_aspect = len(imgs)

cur.execute('SELECT * from audios')
auds = cur.fetchall()
total_auds = len(auds)


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
        return redirect(url_for('views.thank_you'))

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
    global start_time
    start_time = time.time()
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
    time_taken_ = time.time()-start_time
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO data (user_id, session_id, img1, img2, selection,time_taken) VALUES (?, ?, ?, ?, ?,?)",
                (user_id, sess_idntfr, img1, img2, selection,time_taken_))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect(url_for('views.select'))

###################################
# Routes for aspect ratio survey

@views.route('/aspect_select')
@login_required
def aspect_select():
    sess = sess_idntfr  # store the value of session_identifier from home
    cursorObject = conn.cursor()
    cursorObject.execute(
        "SELECT img1, img2 FROM aspect_data WHERE session_id = '{}' ".format(sess))  # select images from the database with same session_id so that they can be removed.
    res = cursorObject.fetchall()

    # make a list of all such rows and delete them
    lis = list(range(1, total_imgs_aspect+1))
    for x in res:
        lis.remove(x[0])
        lis.remove(x[1])

    # if all images are done, render the home page
    if len(lis) == 0:
        return redirect(url_for('views.thank_you'))

    # make random choices and select those images
    i1 = random.choice(lis)
    lis.remove(i1)
    i2 = random.choice(lis)
    cursorObject.execute(
        "SELECT img_id,link FROM aspect_images WHERE img_id={}".format(i1))
    image1 = cursorObject.fetchone()
    cursorObject.execute(
        "SELECT img_id,link FROM aspect_images WHERE img_id={}".format(i2))
    image2 = cursorObject.fetchone()
    global start_time
    start_time = time.time()
    return render_template('aspect_survey.html', img1=image1, img2=image2, user=current_user)

@ views.route('/aspect_submit', methods=['POST'])
@ login_required
def aspect_submit():
    # get the user's selection and the two images that were shown
    user_id = request.form['user_id']
    selection = request.form['selection']
    img1 = request.form['img1']
    img2 = request.form['img2']
    sess_id = request.form['sess_id']
    time_taken_ = time.time()-start_time
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO aspect_data (user_id, session_id, img1, img2, selection,time_taken) VALUES (?, ?, ?, ?, ?,?)",
                (user_id, sess_idntfr, img1, img2, selection,time_taken_))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect(url_for('views.aspect_select'))

############################
#Routes for audio survey
@views.route('/audio_select')
@login_required
def audio_select():
    sess = sess_idntfr  # store the value of session_identifier from home
    cursorObject = conn.cursor()
    cursorObject.execute(
        "SELECT aud1, aud2 FROM audio_data WHERE session_id = '{}' ".format(sess))  # select audios from the database with same session_id so that they can be removed.
    res = cursorObject.fetchall()

    # make a list of all such rows and delete them
    lis = list(range(1, total_auds+1))
    for x in res:
        lis.remove(x[0])
        lis.remove(x[1])

    # if all images are done, render the home page
    if len(lis) == 0:
        return redirect(url_for('views.thank_you'))

    # make random choices and select those images
    i1 = random.choice(lis)
    lis.remove(i1)
    i2 = random.choice(lis)
    cursorObject.execute(
        "SELECT aud_id,link FROM audios WHERE aud_id={}".format(i1))
    a1 = cursorObject.fetchone()
    cursorObject.execute(
        "SELECT aud_id,link FROM audios WHERE aud_id={}".format(i2))
    a2 = cursorObject.fetchone()
    global start_time
    start_time = time.time()
    return render_template('audio_survey.html', aud1=a1, aud2=a2, user=current_user)

@ views.route('/audio_submit', methods=['POST'])
@ login_required
def audio_submit():
    # get the user's selection and the two images that were shown
    user_id = request.form['user_id']
    selection = request.form['selection']
    aud1 = request.form['aud1']
    aud2 = request.form['aud2']
    sess_id = request.form['sess_id']
    time_taken_ = time.time()-start_time
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO audio_data (user_id, session_id, aud1, aud2, selection, time_taken) VALUES (?, ?, ?, ?, ?,?)",
                (user_id, sess_idntfr, aud1, aud2, selection,time_taken_))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect(url_for('views.aspect_select'))


###########################
# Utility routes
@ views.route('/thank_you')
@login_required
def thank_you():
    return render_template("thankyou.html",user= current_user)