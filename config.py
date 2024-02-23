import uuid
from flask import Flask
from flask import render_template, request, redirect, url_for, session, make_response, flash, send_file
from functools import wraps 
import json
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
from datetime import datetime
import random , json, re, time, string, os

import pytz, pymysql
import socket
import hashlib
host = socket.gethostname()
app = Flask(__name__)
a = app.secret_key = str(uuid.uuid4())
if host == 'DESKTOP-V6NL7VS':
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'elaerning'
    app.config['MYSQL_CONNECT_TIMEOUT'] = 600  
else:
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'elaerning'
    app.config['MYSQL_CONNECT_TIMEOUT'] = 600  
mysql = MySQL(app)
conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

try:
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
except pymysql.Error as e:
    print(f"Error connecting to the database: {e}")

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        
        else:
            return make_response(json.dumps({'response': 'Unauthorized access, login required', 'code': 404})), 401
    return decorated_func

# to change on the live server 
def get_time():
    if host == 'DESKTOP-V6NL7VS':
        now = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %I:%M:%S %p")
    else:
        now = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %I:%M:%S %p")
    return now
def get_filecode():
    code = random.randint(1000000, 9999999)
    return code

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['IMG_FOLDER'] = 'static/uploads/'
# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

ALLOWED_PDF = set(['pdf', 'doc', 'docx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PDF

def hash_password(password):
    result = hashlib.sha1("{}".format(password).encode('utf-8')).hexdigest()
    return result

