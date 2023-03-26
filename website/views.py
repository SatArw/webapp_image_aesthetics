from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
# from .models import Selection
from . import db
import json
import time
import uuid

time_between_pairs = 20
session_id = str(uuid.uuid4())
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)
