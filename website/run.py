from flask import Flask, render_template, request, redirect, session, Blueprint
from flask_login import current_user
import sqlite3
import random
import time
import uuid

run = Blueprint('run', __name__)

# connect to the database
conn = sqlite3.connect(
    "/home/satarw/Documents/webapp/img_db", check_same_thread=False)
session_id = str(uuid.uuid4())


@run.route('survey', methods=['GET', 'POST'])
def survey():
    # select two random images from the database
    cur = conn.cursor()
    cur.execute("SELECT img_id, link FROM images ORDER BY RANDOM() LIMIT 2")
    rows = cur.fetchall()
    img1 = rows[0]
    img2 = rows[1]
    # render the survey page with the two images
    return render_template('survey.html', img1=img1, img2=img2, user=current_user)

# process the survey form


@run.route('submit', methods=['GET', 'POST'])
def submit():
    # get the user's selection and the two images that were shown
    selection = request.form['selection']
    img1 = request.form['img1']
    img2 = request.form['img2']
    # insert the data into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO data (user_id, session_id, img1, img2, selection) VALUES (?, ?, ?, ?, ?)",
                (current_user, session_id, img1, img2, selection))
    conn.commit()
    # redirect to the home page to show the next pair of images
    return redirect('/survey')


# @run.route('/survey')
# def index():
#     return render_template('survey.html', user=current_user)


# @run.route('/aspect_ratio_survey')
# def index_one():
#     return render_template('aspect_ratio_survey.html', user=current_user)


# if __name__ == '__run__':
    # run.run(debug=True)
