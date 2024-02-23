from sqlite3 import Row
from config import *

import json
import MySQLdb.cursors
from flask_mysqldb import MySQL
import re
from flask import render_template, request, redirect, url_for, session, make_response,jsonify
from werkzeug.utils import secure_filename
import MySQLdb.cursors
# format currency
@app.template_filter()
def currency_format(value):
    value = float(value)
    return "{:,.0f}".format(value)

#split page
@app.template_filter()
def par_format(value):
    x = value.split(",")
    return x

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM log WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username or password'
            return render_template('login.html', error=msg)
    # Show the login form with message (if any)
    else:
        return render_template('login.html', error=msg)

@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username", None)
        session.pop("name", None)
        return redirect('login')
    else:
        return redirect('login')


@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard/index1.html')
    else:
        return redirect(url_for('login'))

@app.route('/index')
@app.route('/')
def index():
    cursor.execute("SELECT * FROM barner order by barner.bar_id DESC limit 1")
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM topics INNER JOIN subjects on topics.sub_id=subjects.sub_id order by topic_id  DESC limit 3")
    topics= cursor.fetchall()
    res = {"data": rows, "topics" : topics}
    return render_template('index.html', **res)
    
    


@app.route('/about')
def about():
        return render_template('about.html',)

@app.route('/subject_list')
def subject_list():
    cursor.execute("SELECT * FROM topics INNER JOIN subjects on topics.sub_id=subjects.sub_id order by topic_id  DESC")
    topicz= cursor.fetchall()
    return render_template('subject_list.html', topicz=topicz)

@app.route('/course_details')
def course_details():
        return render_template('course_details.html',)

@app.route('/blog')
def blog():
        return render_template('blog.html',)

@app.route('/blog_single')
def blog_single():
        return render_template('blog_single.html',)

@app.route('/contact')
def contact():
        return render_template('contact.html',)



@app.route('/register', methods=['POST', 'GET'])
def register():
    # `students_id`, `full_name`, `class`, `address`, `parent_name`, `contact`, `username`, `password`
    msg = ''
    if request.method == 'POST':
        fn= request.form['full_name']
        cl= request.form['class']
        ad= request.form['address']
        pa= request.form['parent_name']
        con= request.form['contact']
        us= request.form['username']
        pas= request.form['password']
               
    # creating variable for connection
        y = cursor.execute(
            'INSERT INTO   students(`full_name`, `class`, `address`, `parent_name`, `contact`, `username`, `password`) VALUES(%s, %s,  %s,  %s, %s, %s, %s)', (fn, cl, ad, pa, con, us, pas))
        conn.commit()
        if y:
    # displaying message
            res = {'msg': 'You have successfully registered !'}
            return redirect(url_for('login'))
        else:
            res = {'msg': 'Record not  registered'}
            return render_template('register.html', **res)
    else:
         
         cursor.execute("SELECT * FROM   subjects")
         data = cursor.fetchall()
         response = {'data': data, 'status': 'true', }
         return render_template('register.html', **response)


@app.route('/students', methods=['POST', 'GET'])
def students():
        cursor.execute("SELECT * FROM   students")
        data = cursor.fetchall()
        response = {'data': data, 'status': 'true', }
        return render_template('dashboard/students.html', **response)






@app.route('/slider', methods=['POST', 'GET'])
def slider():
    #`bar_id`, `name`, `img`, `description`
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.split(".")[-1]
            filename = '{}.{}'.format(get_filecode(), file_ext)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            name = request.form['name']
            description = request.form['description']
            img = app.config['IMG_FOLDER'] + str(filename)
            cursor.execute("SELECT * FROM barner WHERE name=%s LIMIT 1", (name, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO barner(name,img,description ) " \
                            "VALUES(%s, %s, %s)"
                bind_data = (name, img, description)
                cursor.execute(sql_query, bind_data)
                conn.commit()
                flash('Record successfully added')
                return redirect(url_for('slider'))
            else:
                flash('Records already registered')
                return redirect(url_for('slider'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor.execute("SELECT * FROM barner")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('slider.html', **res)


@app.route('/subjects', methods=['POST', 'GET'])
def subjects():
    # `cat_id`, `date`, `category`
    msg = ''
    if request.method == 'POST':
        dt= get_time()
        d= request.form['subjects']
        ot= request.form['outline']
        des= request.form['description']
               
    # creating variable for connection
        y = cursor.execute(
            'INSERT INTO   subjects(`date`, `subjects`, `outline`, `description`) VALUES(%s, %s,  %s,  %s)', (dt, d, ot, des))
        conn.commit()
        if y:
    # displaying message
            res = {'msg': 'You have successfully registered !'}
            return redirect(url_for('subjects'))
        else:
            res = {'msg': 'Record not  registered'}
            return render_template('dashboard/category.html', **res)
    else:
         
         cursor.execute("SELECT * FROM   subjects")
         data = cursor.fetchall()
         response = {'data': data, 'status': 'true', }
         return render_template('dashboard/subjects.html', **response)

@app.route('/delet/<catid>', methods=['POST', 'GET'])
def delet(catid):
        cursor.execute("DELETE FROM subjects WHERE  subjects_id=%s", (catid))
        conn.commit()
        return redirect('dashboard/subjects')



@app.route('/topics', methods=['POST', 'GET'])
def topics():
    #`bar_id`, `name`, `img`, `description`
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.split(".")[-1]
            filename = '{}.{}'.format(get_filecode(), file_ext)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            catid = str(request.form['sub_id'])
            class1 = request.form['class1']
            term = request.form['term']
            body = request.form['body']
            duration = request.form['duration']
            img = app.config['IMG_FOLDER'] + str(filename)
            cursor.execute("SELECT * FROM topics WHERE body=%s LIMIT 1", (body, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO topics (class1, term, body,img,duration,sub_id) " \
                            "VALUES(%s, %s, %s, %s, %s, %s)"
                bind_data = (class1, term, body,img,duration,catid)
                cursor.execute(sql_query, bind_data)
                conn.commit()
                flash('Record successfully added')
                return redirect(url_for('topics'))
            else:
                flash('Records already registered')
                return redirect(url_for('topics'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor.execute("SELECT * FROM topics INNER JOIN subjects on topics.sub_id=subjects.sub_id order by topics.topic_id DESC")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM subjects order by sub_id")
        rows = cursor.fetchall()
        response = {'data' :data, 'status': 'true', 'rows': rows}
        return render_template('dashboard/topics.html', **response)


@app.route('/results', methods=['POST', 'GET'])
def results():
    # `results_id`, `term_one`, `term_two`, `term_three`, `students_id`
    msg = ''
    if request.method == 'POST':
        catid = str(request.form['students_id'])
        dt= request.form['term_one']
        ot= request.form['term_two']
        des= request.form['term_three']
        com= request.form['comments']
               
    # creating variable for connection
        y = cursor.execute(
            'INSERT INTO   results(`term_one`, `term_two`, `term_three`, `students_id`, `comments` ) VALUES(%s, %s,  %s,  %s, %s)', (dt, ot, des, com, catid))
        conn.commit()
        if y:
    # displaying message
            res = {'msg': 'You have successfully registered !'}
            return redirect(url_for('results'))
        else:
            res = {'msg': 'Record not  registered'}
            return render_template('dashboard/results.html', **res)
    else:
        cursor.execute("SELECT * FROM results INNER JOIN students on results.students_id=students.students_id order by results.results_id DESC")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM students order by full_name")
        rows = cursor.fetchall()
        response = {'data' :data, 'status': 'true', 'rows': rows}
        return render_template('dashboard/topics.html', **response)





        cursor.execute("SELECT * FROM   results INNER JOIN students on results.students_id=students.students_id")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM students order by full_name")
        rows = cursor.fetchall()
        response = {'data': data, 'status': 'true', 'rows' : rows}
        return render_template('dashboard/results.html', **response)





if __name__ == '__main__':
    app.run(port=5000, debug=True)

