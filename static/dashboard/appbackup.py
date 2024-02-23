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
    


@app.route('/clients', methods=['POST', 'GET'])
def clients():
    #``client_id`, `name`, `username`, `img`, `email`, `password`, `confirm`, `number`, `contact`, `company`
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
            username = request.form['username']
            position = request.form['position']
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm']
            number = request.form['number']
            contact = request.form['contact']
            company = request.form['company']
            img = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM client WHERE name=%s LIMIT 1", (name, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO client(name,img,username, email, password, confirm, number, contact, company, position ) " \
                            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                bind_data = (name, img, username, email, password, confirm, number,  contact, company, position)
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('clients'))
            else:
                flash('Records already registered')
                return redirect(url_for('clients'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM  client order by client.client_id DESC")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('clients.html', **res)

@app.route('/clients_list')
def clients_list():
    return render_template('clients_list.html')

@app.route('/clients_profile')
def clients_profile():
    return render_template('clients_profile.html')

@app.route('/employees', methods=['POST', 'GET'])
def employees():
    #`expense_id`, `fname`, `lname`, `username`, `email`, `password`, `number`, `date`, `phone`, `image`, `department`, `designation`
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
            fname = request.form['fname']
            lname = request.form['lname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            retype = request.form['retype']
            number = request.form['number']
            date = request.form['date']
            phone = request.form['phone']
            department = request.form['department']
            bank = request.form['bank']
            designation = request.form['designation']
            account = request.form['account']
            image = app.config['IMG_FOLDER'] + str(filename)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM employees WHERE fname=%s LIMIT 1", (fname, ))
            rows = cursor.fetchone()
            if not rows:
                sql_query = "INSERT INTO employees(lname,fname,img,username, email, password, retype, number, date, phone, department, designation, bank, account ) " \
                            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s)"
                bind_data = (lname, fname, image, username, email, password, retype, number, date, phone, department, designation, bank, account )
                cursor.execute(sql_query, bind_data)
                mysql.connection.commit()
                flash('Record successfully added')
                return redirect(url_for('employees'))
            else:
                flash('Records already registered')
                return redirect(url_for('employees'))
        else:
            flash('Allowed file types png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM  employees order by employees.employ_id DESC")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('employees.html', **res)
    

@app.route('/holidays',methods=['POST','GET'])
def holidays():
    #`hol_id`, `holiday`, `date`, `day`
    msg=''
    #applying empty validation
    if request.method == 'POST':

        #passing HTML form data into python variable.
        f = request.form['holiday']
        c = request.form['date']
        a = request.form['day']
            

        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM  holly' )
        #fetching data from MySQL
        # result = cursor.fetchone()
        # if result:
        #     msg = 'Name already exists !'
        # else:
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO  holly VALUES (NULL, %s, %s, %s)', (f, c, a))
        mysql.connection.commit()
        
        #displaying message
        msg = 'You have successfully registered !'
        res = {'msg': 'You have successfully registered !'}
        return redirect('/holidays')
        # return render_template('students-records.html')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM holly order by holiday")
        data = cursor.fetchall()
        response = {'data': data, 'status': 'true',}
        return render_template('holidays.html', **response)

@app.route('/leaves_employee', methods=['POST','GET'])
def leaves_employee():
    return render_template('leaves_employee.html')

@app.route('/leaves', methods=['POST', 'GET'])
def leaves():
    # `lev_id`, `leav`, `date1`, `date2`, `days`, `reason`, `employ_id`
    msg = ''
    # applying empty validation
    if request.method == 'POST':
        # passing HTML form data into python variable.
        stafid = str(request.form['employ_id'])
        d= request.form['leav']
        f = request.form['date1']
        a = request.form['date2']
        b = request.form['days']
        c = request.form['reason']
        
       # creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        y = cursor.execute(
            'INSERT INTO   leave_admin VALUES(NULL, %s, %s,  %s, %s, %s, %s)', (d, f, a, b, c, stafid,))
        mysql.connection.commit()
        if y:
            # displaying message
            res = {'msg': 'Asses successfully registered !'}
            return redirect('/leaves')
        else:
            res = {'msg': 'Record not  registered'}
            return render_template('leaves.html', **res)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM   leave_admin INNER JOIN employees on  leave_admin.employ_id=employees.employ_id")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM employees order by fname ")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM  employees order by employees.employ_id DESC")
        leaves = cursor.fetchall()
        response = {'data': data, 'status': 'true', 'rows' : rows, }
        return render_template('leaves.html', **response)




@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/overtime', methods=['POST', 'GET'])
def overtime():
    # `over_id`, `date3`, `hour`, `type`, `description`, `approved`, `employ_id`
    msg = ''
    # applying empty validation
    if request.method == 'POST':
        # passing HTML form data into python variable.
        stafid = str(request.form['employ_id'])
        d= request.form['date3']
        f = request.form['hour']
        a = request.form['type']
        b = request.form['description']
        c = request.form['approved']
       
        
       # creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        y = cursor.execute(
            'INSERT INTO   overtime VALUES(NULL, %s, %s, %s, %s, %s, %s)', (d, f, a, b, c, stafid,))
        mysql.connection.commit()
        if y:
            # displaying message
            res = {'msg': 'Asses successfully registered !'}
            return redirect('/overtime')
        else:
            res = {'msg': 'Record not  registered'}
            return render_template('overtime.html', **res)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM   overtime INNER JOIN employees on  overtime.employ_id=employees.employ_id")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM employees order by fname ")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM  employees order by employees.employ_id DESC")
        leaves = cursor.fetchall()
        response = {'data': data, 'status': 'true', 'rows' : rows, }
        return render_template('overtime.html', **response)



@app.route('/shift_scheduling')
def shift_scheduling():
    return render_template('shift_scheduling.html')

@app.route('/shift_list')
def shift_list():
    return render_template('shift_list.html')

@app.route('/timesheet')
def timesheet():
    return render_template('timesheet.html')

@app.route('/leave_settings')
def leave_settings():
    return render_template('leave_settings.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/attendance_employee')
def attendance_employee():
    return render_template('attendance_employee.html')

@app.route('/departments',methods=['POST','GET'])
def departments():
    #`hol_id`, `holiday`, `date`, `day`
    msg=''
    #applying empty validation
    if request.method == 'POST':

        #passing HTML form data into python variable.
        f = request.form['name']
        c = request.form['head']
       
       #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM  depart' )
        
        #fetching data from MySQL
        cursor.execute('INSERT INTO  depart VALUES (NULL, %s, %s)', (f, c))
        mysql.connection.commit()
        
        #displaying message
        msg = 'You have successfully registered !'
        res = {'msg': 'You have successfully registered !'}
        return redirect('/departments')
        
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM depart order by name")
        data = cursor.fetchall()
        response = {'data': data, 'status': 'true',}
        return render_template('departments.html', **response)

@app.route('/designations')
def designations():
    return render_template('designations.html')

@app.route('/file_manager')
def file_manager():
    return render_template('file_manager.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/projects',methods=['POST','GET'])
def projects():
    #pro_id`, `project`, `client`, `start`, `end`, `leader`, `members`, `description`
    msg=''
    #applying empty validation
    if request.method == 'POST':

        #passing HTML form data into python variable.
        a = request.form['project']
        b = request.form['client']
        d = request.form['start']
        e = request.form['end']
        f = request.form['leader']
        g = request.form['members']
        h = request.form['description']
            

        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM  projects' )
        #fetching data from MySQL
        # result = cursor.fetchone()
        # if result:
        #     msg = 'Name already exists !'
        # else:
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO  projects VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)', (a, b, d, e, f, g, h))
        mysql.connection.commit()
        
        #displaying message
        msg = 'You have successfully registered !'
        res = {'msg': 'You have successfully registered !'}
        return redirect('/projects')
        # return render_template('students-records.html')
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM  projects order by projects.pro_id DESC")
        rows = cursor.fetchall()
        res = {"data": rows, }
        return render_template('projects.html', **res)


@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/project_view')
def project_view():
    return render_template('project_view.html')

@app.route('/project_list')
def project_list():
    return render_template('project_list.html')

@app.route('/task_board')
def task_board():
    return render_template('task_board.html')

@app.route('/task_view')
def task_view():
    return render_template('task_view.html')

@app.route('/leads')
def leads():
    return render_template('leads.html')

@app.route('/tickets')
def tickets():
    return render_template('tickets.html')

@app.route('/estimates')
def estimates():
    return render_template('estimates.html')

@app.route('/create_estimate',methods=['POST','GET'])
def create_estimate():
    #``cret_id`, estnumber, `client`, `project`, `email`, `tax`, `address`, `billing`, `estimate`, `expiry`, `item`, `description`, `unit`, `quantity`, `amount`, `total`, `other`
    msg=''
    #applying empty validation
    if request.method == 'POST':

        #passing HTML form data into python variable.
        est = request.form['estnumber']
        cl = request.form['client']
        p = request.form['project']
        a = request.form['email']
        b = request.form['tax']
        d = request.form['address']
        e = request.form['billing']
        f = request.form['estimate']
        g = request.form['expiry']
        h = request.form['item']
        i = request.form['description']
        j = request.form['unit']
        k = float(request.form['quantity'])
        l = float(request.form['amount'])
        m = k * l
        n = request.form['other']
            

        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM  create_estimate' )
        #fetching data from MySQL
        # result = cursor.fetchone()
        # if result:
        #     msg = 'Name already exists !'
        # else:
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO  create_estimate VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (est, cl, p, a, b, d, e, f, g, h, i, j, k, l, m, n))
        mysql.connection.commit()
        
        #displaying message
        msg = 'You have successfully registered !'
        res = {'msg': 'You have successfully registered !'}
        return redirect('/estimate_view')
        # return render_template('students-records.html')
    else:
        return render_template('create_estimate.html', mgs=msg)


@app.route('/estimate_view')
def estimate_view():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM  create_estimate order by create_estimate.cret_id DESC")
    estimate_view = cursor.fetchall()
    return render_template('estimate_view.html', estimate_view=estimate_view)
   

@app.route('/invoices')
def invoices():
    return render_template('invoices.html')

@app.route('/invoice_view')
def invoice_view():
    return render_template('invoice_view.html')

@app.route('/edit_invoice')
def edit_invoice():
    return render_template('edit_invoice.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/provident_fund')
def provident_fund():
    return render_template('provident_fund.html')

@app.route('/taxes')
def taxes():
    return render_template('taxes.html')


@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')   

@app.route('/employees_list')
def employees_list():
    return render_template('employees_list.html')  

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')  

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/budgets')
def budgets():
    return render_template('budgets.html')

@app.route('/budget_expenses')
def budget_expenses():
    return render_template('budget_expenses.html')

@app.route('/budget_revenues')
def budget_revenues():
    return render_template('budget_revenues.html')

@app.route('/salary')
def salary():
    return render_template('salary.html')

@app.route('/salary_view')
def salary_view():
    return render_template('payroll_items.html')

@app.route('/payroll-items')
def payroll_items():
    return render_template('payroll_items.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/expense_reports')
def expense_reports():
    return render_template('expense_reports.html')

@app.route('/invoice_reports')
def invoice_reports():
    return render_template('invoice_reports.html')


@app.route('/payments_reports')
def payments_reports():
    return render_template('payments_reports.html')

@app.route('/project_reports')
def project_reports():
    return render_template('project_reports.html')

@app.route('/task_reports')
def task_reports():
    return render_template('task_reports.html')


@app.route('/user_reports')
def user_reports():
    return render_template('user_reports.html')

@app.route('/employee_reports')
def employee_reports():
    return render_template('employee_reports.html')

@app.route('/payslip_reports')
def payslip_reports():
    return render_template('payslip_reports.html')

@app.route('/performance_indicator')
def performance_indicator():
    return render_template('performance_indicator.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/appraisal')
def appraisal():
    return render_template('appraisal.html')

@app.route('/goal_tracking')
def goal_tracking():
    return render_template('goal_tracking.html')

@app.route('/goal_type')
def goal_type():
    return render_template('goal_type.html')

@app.route('/attendance_reports')
def attendance_reports():
    return render_template('attendance_reports.html')




if __name__ == '__main__':
    app.run(port=5000, debug=True)