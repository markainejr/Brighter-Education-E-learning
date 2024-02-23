from sqlite3 import Row
from config import *
from flask import render_template, request, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename

import MySQLdb.cursors
# format currency
@app.template_filter()
def currency_format(value):
    value = float(value)
    return "{:,.0f}".format(value)

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

@app.route('/index')
@app.route('/')
def index():
    if "username" in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM log WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['std_id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('index'))
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM barner WHERE name=%s LIMIT 1", (name, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO barner(name,img,description ) " \
                            "VALUES(%s, %s, %s)"
                bind_data = (name, img, description)
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('slider'))
            else:
                flash('Records already registered')
                return redirect(url_for('slider'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM barner")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('slider.html', **res)



@app.route('/subjects', methods=['POST', 'GET'])
def subjects():
    # `cat_id`, `date`, `category`
    msg = ''
    # applying empty validation
    if request.method == 'POST':
        # passing HTML form data into python variable.
        dt= get_time()
        d= request.form['subjects']
               
    # creating variable for connection
        y = cursor.execute(
            'INSERT INTO   subjects(`date`, `subjects`) VALUES(%s, %s)', (dt, d))
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

@app.route('/delete/<catid>', methods=['POST', 'GET'])
def gal_entry(catid):
        cursor.execute("DELETE FROM subjects WHERE  subjects_id=%s", (catid))
        conn.commit()
        return redirect('/subjects')





@app.route('/scope', methods=['POST', 'GET'])
def scope():
    #``curriculum_id`, `subject`, `img`, `details`
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
            subject = request.form['subject']
            details = request.form['details']
            img = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM curriculum WHERE subject=%s LIMIT 1", (subject, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO curriculum(subject,img,details ) " \
                            "VALUES(%s, %s, %s)"
                bind_data = (subject, img, details)
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('scope'))
            else:
                flash('Records already registered')
                return redirect(url_for('scope'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM curriculum")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('scope.html', **res)

@app.route('/blog1', methods=['POST', 'GET'])
@login_required
def blog1():
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
            header = request.form['header']
            category = request.form['category']
            body = request.form['body']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM blog WHERE header=%s LIMIT 1", (header, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO blog(category,header,img,body) " \
                            "VALUES(%s, %s, %s, %s)"
                bind_data = (category, header, image, body, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('blog1'))
            else:
                flash('Records already registered')
                return redirect(url_for('blog1'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM blog")
        data = cursor.fetchall()
        return render_template('blog1.html', data=data)
    
@app.route('/bog/<blogid>', methods=['POST', 'GET'])
def blog_entry(blogid):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM blog WHERE  blog_id=%s", (blogid))
        mysql.connection.commit()
        return redirect('/blog1')




@app.route('/teachers', methods=['POST', 'GET'])
def teachers():
    #``teach_id`, `fullname`, `subject`, `img`, `description`, `contact``
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
            fullname = request.form['fullname']
            subject = request.form['subject']
            description = request.form['description']
            contact = request.form['contact']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM teachers WHERE fullname=%s LIMIT 1", (fullname, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO teachers(fullname, subject, img,description, contact ) " \
                            "VALUES(%s, %s, %s, %s, %s)"
                bind_data = (fullname, subject, image, description, contact )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('teachers'))
            else:
                flash('Records already registered')
                return redirect(url_for('teachers'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM  teachers")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('teachers.html', **res)

@app.route('/gallery1', methods=['POST', 'GET'])
@login_required
def gallery1():
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
            title = request.form['title']
            event = request.form['event']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM gallerys WHERE title=%s LIMIT 1", (title, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO gallerys(title,img,event) " \
                            "VALUES(%s, %s, %s)"
                bind_data = (title, image, event, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('gallery1'))
            else:
                flash('Records already registered')
                return redirect(url_for('gallery1'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM gallerys")
        data = cursor.fetchall()
        return render_template('gallery1.html', data=data)
    
@app.route('/gale/<galid>', methods=['POST', 'GET'])
def gallery_entry(galid):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM gallerys WHERE  gal_id=%s", (galid))
        mysql.connection.commit()
        return redirect('/gallery1') 


@app.route('/store', methods=['POST', 'GET'])
@login_required
def store():
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
            date= get_time()
            item = request.form['item']
            details = request.form['details']
            price = request.form['price']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM stores WHERE item=%s LIMIT 1", (item, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO stores (date,item,img,details,price) " \
                            "VALUES(%s, %s, %s, %s, %s)"
                bind_data = (date, item, image, details, price, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('store'))
            else:
                flash('Records already registered')
                return redirect(url_for('store'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM stores")
        data = cursor.fetchall()
        return render_template('store.html', data=data)



@app.route('/del/<storeid>', methods=['POST', 'GET'])
def dele_entry(storeid):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM stores WHERE  serve_id=%s", (serveid,))
        mysql.connection.commit()
        return redirect('/store')


@app.route('/smc1', methods=['POST', 'GET'])
@login_required
def smc1():
    if request.method == 'POST':
        # check if the post request has the file part ...`com_id`, `date`, `fname`, `img`, `title`, `details`
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
            date= get_time()
            fname = request.form['fname']
            details = request.form['details']
            title = request.form['title']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM committe WHERE fname=%s LIMIT 1", (fname, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO committe (date,fname,img,details,title) " \
                            "VALUES(%s, %s, %s, %s, %s)"
                bind_data = (date, fname, image, details, title, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('smc1'))
            else:
                flash('Records already registered')
                return redirect(url_for('smc1'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM committe")
        data = cursor.fetchall()
        return render_template('smc1.html', data=data)



@app.route('/del/<storeid>', methods=['POST', 'GET'])
def dele_ntry(storeid):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM stores WHERE  serve_id=%s", (serveid,))
        mysql.connection.commit()
        return redirect('/smc1')


@app.route('/pta1', methods=['POST', 'GET'])
@login_required
def pta1():
    if request.method == 'POST':
        # check if the post request has the file part ...`com_id`, `date`, `fname`, `img`, `title`, `details`
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
            date= get_time()
            name = request.form['name']
            details = request.form['details']
            title = request.form['title']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM pta WHERE name=%s LIMIT 1", (name, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO pta (date,name,img,details,title) " \
                            "VALUES(%s, %s, %s, %s, %s)"
                bind_data = (date, name, image, details, title, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('pta1'))
            else:
                flash('Records already registered')
                return redirect(url_for('pta1'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM pta")
        data = cursor.fetchall()
        return render_template('pta1.html', data=data)



@app.route('/del/<storeid>', methods=['POST', 'GET'])
def dele_try(storeid):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM pta WHERE  pta_id=%s", (serveid,))
        mysql.connection.commit()
        return redirect('/pta')


@app.route('/prefects', methods=['POST', 'GET'])
@login_required
def prefects():
    if request.method == 'POST':
        # check if the post request has the file part ...`com_id`, `date`, `fname`, `img`, `title`, `details`
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
            date= get_time()
            fullname = request.form['fullname']
            details = request.form['details']
            title = request.form['title']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM prefects WHERE fullname=%s LIMIT 1", (fullname, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO prefects (date,fullname,img,details,title) " \
                            "VALUES(%s, %s, %s, %s, %s)"
                bind_data = (date, fullname, image, details, title, )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('prefects'))
            else:
                flash('Records already registered')
                return redirect(url_for('prefects'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM prefects")
        data = cursor.fetchall()
        return render_template('prefects.html', data=data)



@app.route('/del/<storeid>', methods=['POST', 'GET'])
def dele_prefects(storeid):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM prefects WHERE  pre_id=%s", (serveid,))
        mysql.connection.commit()
        return redirect('/prefects')


   

@app.route('/invoices')
def invoices():
    return render_template('invoices.html')

@app.route('/invoice_view')
def invoice_view():
    return render_template('invoice_view.html')




if __name__ == '__main__':
    app.run(port=5000, debug=True)