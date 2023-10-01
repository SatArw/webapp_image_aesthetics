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

time_between_pairs = 3
time_for_each_pair = 5
max_pairs_in_session = 20
views = Blueprint('views', __name__)

conn = sqlite3.connect(
    "img_db", check_same_thread=False)

cur = conn.cursor()
cur.execute('SELECT * FROM images')
imgs = cur.fetchall()


cur.execute('SELECT * FROM aspect_images')
imgs = cur.fetchall()
total_imgs = len(imgs)

cur.execute('SELECT * from audios')
auds = cur.fetchall()
total_auds = len(auds)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global sess_idntfr, global_time
    global_time = time.time()
    sess_idntfr = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=10))
    return render_template("home.html", user=current_user, sid=sess_idntfr)


@views.route('/select')
@login_required
def select():
    try:
        sess = sess_idntfr  # store the value of session_identifier from home
    except:
        flash('Something went wrong with the session! Please try again',category='error')
        render_template(url_for('views.home'))

    survey_type = session.get('survey_type')
    if survey_type is None: #if survey_type is none, it means select is being called from home and we need to request it from the form.
        survey_type = request.args.get('survey') #if survey_type is already stored in the session, then no need to request
        session['survey_type'] = survey_type    

    #setting the right table to insert into
    if survey_type == 'temple':
        table_name = 'data'
    elif survey_type == 'aspect':
        table_name = 'aspect_data'
    else:
        return redirect(url_for('views.home'))
    
    cursorObject = conn.cursor()
    try:
        cursorObject.execute(f"SELECT img1, img2 FROM {table_name} WHERE session_id ='{sess}' ")  # select images from the database with same session_id so that they can be removed.
    except:
        flash('Something went wrong with the database! Please re-take the survey',category='error')
        redirect(url_for('views.home'))
    res = cursorObject.fetchall()
    sess_limit = True if len(res) == max_pairs_in_session else False
    # make a list of all such rows and delete them
    lis = list(range(1, total_imgs+1)
               )
    
    for x in res:
        print(x[0],x[1])
        if x[0] in lis:
            lis.remove(x[0])
        if x[1] in lis:
            lis.remove(x[1])

    # if all images are done, render the home page
    login_timeout = max_pairs_in_session * time_for_each_pair + 3
    if len(lis) == 0 or sess_limit or (time.time()-global_time >= login_timeout):
        session.pop('survey_type')
        return redirect(url_for('views.thank_you'))

    if table_name == 'data': table_name = 'images'
    if table_name == 'aspect_data': table_name = 'aspect_images'

    # make random choices and select those images
    i1 = random.choice(lis)
    lis.remove(i1)
    i2 = random.choice(lis)
    try:
        cursorObject.execute(
        f"SELECT img_id,link FROM {table_name} WHERE img_id={i1}")
    except:
        flash('Something went wrong with the database! Please re-take the survey',category='error')
        redirect(url_for('views.home'))
    image1 = cursorObject.fetchone()
    try:
        cursorObject.execute(
        f"SELECT img_id,link FROM {table_name} WHERE img_id={i2}")
    except:
        flash('Something went wrong with the database! Please re-take the survey',category='error')
        redirect(url_for('views.home'))   
    image2 = cursorObject.fetchone()
    global start_time
    start_time = time.time()
    return render_template('survey.html', img1=image1, img2=image2, user=current_user,survey_type=survey_type)

@ views.route('/submit', methods=['POST'])
@ login_required
def submit():
    # get the user's selection and the two images that were shown
    user_id = request.form['user_id']
    selection = request.form['selection']
    img1 = request.form['img1']
    img2 = request.form['img2']
    try:
        time_taken_ = time.time()-start_time
    except:
        flash('Something went wrong with the timer! Please re-take the survey',category='error')
        return redirect(url_for('views.home'))

    survey_type = request.form['survey']  # Get the survey type from the submitted form data

    if survey_type == 'temple':
        table_name = 'data'
    elif survey_type == 'aspect':
        table_name = 'aspect_data'
    else:
        flash('Something went wrong with the database! Please re-take the survey',category='error')
        return redirect(url_for('views.home',survey_type=survey_type))
    
    time.sleep(time_between_pairs)  
    # insert the data into the database
    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO {table_name} (user_id, session_id, img1, img2, selection,time_taken) VALUES (?, ?, ?, ?, ?,?)",
                (user_id, sess_idntfr, img1, img2, selection,time_taken_))
    except:
        flash('Something went wrong with the database! Please re-take the survey',category='error')
        redirect(url_for('views.home'))
    conn.commit()
    # redirect to the home page to show the next pair of images
    
    return redirect(url_for('views.select',survey_type=survey_type))

########################
#Routes for audio survey

# @views.route('/audio_select')
# @login_required
# def audio_select():
#     sess = sess_idntfr  # store the value of session_identifier from home
#     cursorObject = conn.cursor()
#     cursorObject.execute(
#         "SELECT aud1, aud2 FROM audio_data WHERE session_id = '{}' ".format(sess))  # select audios from the database with same session_id so that they can be removed.
#     res = cursorObject.fetchall()
#     sess_limit = True if len(res) == max_pairs_in_session else False
#     # make a list of all such rows and delete them
#     lis = list(range(1, total_auds+1))
    
#     for x in res:
#         lis.remove(x[0])
#         lis.remove(x[1])

#     # if all audios are done, render the home page
#     if len(lis) == 0 or sess_limit:
#         return redirect(url_for('views.thank_you'))

#     # make random choices and select those audios
#     i1 = random.choice(lis)
#     lis.remove(i1)
#     i2 = random.choice(lis)
#     cursorObject.execute(
#         "SELECT aud_id,link FROM audios WHERE aud_id={}".format(i1))
#     a1 = cursorObject.fetchone()
#     cursorObject.execute(
#         "SELECT aud_id,link FROM audios WHERE aud_id={}".format(i2))
#     a2 = cursorObject.fetchone()
#     global start_time
#     start_time = time.time()
#     return render_template('audio_survey.html', aud1=a1, aud2=a2, user=current_user)

# @ views.route('/audio_submit', methods=['POST'])
# @ login_required
# def audio_submit():
#     # get the user's selection and the two audios that were shown
#     user_id = request.form['user_id']
#     selection = request.form['selection']
#     aud1 = request.form['aud1']
#     aud2 = request.form['aud2']
#     sess_id = request.form['sess_id']
#     time_taken_ = time.time()-start_time
#     # insert the data into the database
#     cur = conn.cursor()
#     cur.execute("INSERT INTO audio_data (user_id, session_id, aud1, aud2, selection, time_taken) VALUES (?, ?, ?, ?, ?,?)",
#                 (user_id, sess_idntfr, aud1, aud2, selection,time_taken_))
#     conn.commit()
#     # redirect to the survey page to show the next pair of audios
#     return redirect(url_for('views.audio_select'))

@ views.route('/thank_you')
@login_required
def thank_you():
    return render_template("thankyou.html",user= current_user)