# importing all the necessary python libraries for the application
from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
from datetime import datetime
from key import secret_key,salt,salt2
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from cmail import sendmail
#from flask_mail import Mail, Message

# WSGI application
app = Flask(__name__)

# To configure access to your MySQL database server by using these settings
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = 'Admin'
app.config['MYSQL_DB'] = "CES"

# Initialize the MySQL instance to the variable and pass the WSGI application as an argument to the instance.
mysql = MySQL(app)

# Secret key is used to sign session cookies for protection against cookie data tampering. It's very important that an attacker doesn't know the value of this secret key. 
app.secret_key=secret_key
app.config['SESSION_TYPE']='filesystem'

# Initialize the Bcrypt instance to the variable and pass the WSGI application as an argument to the instance for hashing the password in database.
bcrypt = Bcrypt(app)

# Flask-Mail is configured through the standard Flask config API. The following are the available options to configure flask-mail.
# app.config['MPOAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_RT'] = 465
# app.config['MAIL_USERNAME'] = config.email
# app.config['MAIL_PASSWORD'] = config.password
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = False

# Initialize the Mail instance to the variable and pass the WSGI application as an argument to the instance for sending email from the application.
# mail = Mail(app)


@app.route('/')
def intropage():
    """
    This function render and returns the introduction page of the application.

    Returns
    -------
    TYPE
        html : It returns the intropage.html file

    """
    return render_template('intropage.html')


@app.route('/home')
def home():
    """
    This function render and returns the home page for the users after logged into the application.
    
    This home function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it returns the homepage for the user else it redirects the user to the admin page.

    Returns
    -------
    TYPE
        html : It returns the home.html file

    """
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            userid = session['user_id']
            email = session['email']
            return render_template('home.html',userid=userid,email=email)
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin.html'))

@app.route('/signup', methods=['POST','GET'])
def signup():
    """
    This function render and returns the signup page for the users.
    
    This signup function checks whether the request method is POST or not.
    If it is a POST request, it store all information in the form into the MySQL database and redirects the user into signin page.
    

    Returns
    -------
    TYPE
        html : It returns the signup.html file.

    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor = mysql.connection.cursor()
        cursor.execute('select count(*) from users where email=%s',[email])
        count = cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('Email already in use')
            return render_template('signup.html')
        data={'password':password,'email':email,'confirm_password':confirm_password}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('signin'))
        '''cursor.execute('SELECT * FROM users WHERE email = % s', [email])
        account = cursor.fetchone()
        
        if account:
            message="Account already exists...Try with different email address"
        elif password!=confirm_password:
            message="Your Password and Confirm Password not matched. Please type correct password..."
        else:
            # hashing the password and confirm password before storing it into the database.
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
            hash_confirm_password = bcrypt.generate_password_hash(confirm_password).decode('utf-8')
            
            # create a connection with mysql database using cursor and store the values into the database.
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users(email,password,confirm_password) VALUES(% s,% s,% s)',(email,hash_password,hash_confirm_password))
            mysql.connection.commit()
            
            # send a email to the user regarding account confirmation
            """message="Your account has been created! You are now able to log in"
            msg = Message('Registration Successfull for College Enquiry System',sender=config.email,
                recipients=[email]
            )
            msg.body = f'
            Hello {email}, Welcome to our College Enquiry System!!!
            Your account has been created Successfully. Now you can login into your account and enquire the courses you want.
            Thankyou.
            '
            mail.send(msg)"""
            
            return redirect(url_for('signin'))'''
    
    return render_template('signup.html')

@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor = mysql.connection.cursor()
        email=data['email']
        cursor.execute('select count(*) from users where email=%s',[email])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('signin'))
        else:
            cursor.execute('insert into users(email,password,confirm_password) values(% s,%s,%s)',[data['email'],data['password'],data['confirm_password']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('signin'))

@app.route('/signin',methods=['POST','GET'])
def signin():
    admin_email='admin@codegnan.com'
    apassword='123'
    message=""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        if email==admin_email and password==apassword:
            session['is_admin'] = 1
            session['loggedin'] = True
            return redirect(url_for('admin'))
        else:
            message="1Log in Unsuccessful. Please check username and password"

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = % s',[email])
        user = cursor.fetchone()
        
        if user and password:
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['loggedin'] = True
            return redirect(url_for('home')) 
        else:
            message="Log in Unsuccessful. Please check username and password"
        
    
    return render_template("signin.html",message=message)
#forgetpassword details
@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('select count(*) from users where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT email from users where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(email,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('signin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor = mysql.connection.cursor()
                cursor.execute('update users set password=%s where email=%s',[newpassword,email])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('signin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/logout')
def logout():
    """
    This function helps the user to logout from the application.
    
    This logout function helps the user to logout from the application by
    popping all the values stored in the session and redirects to the signin page.

    Returns
    -------
    TYPE
        html  : It returns the signin.html page.

    """
    session.pop('loggedin', None) 
    session.pop('user_id',None)
    session.pop('is_admin',None)
    session.pop('email',None)
    return redirect(url_for('signin'))

@app.route('/admin')
def admin():
    """
    This function render and returns the admin page for the admin after loggedin with the admin credentials.
    
    This admin function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it returns the adminpage for the user else it redirects the user to the home page.

    Returns
    -------
    TYPE
        html : It returns the admin.html file.

    """
    
    if 'loggedin' in session:
        if session['is_admin'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM seat_availability")
            courselist = cursor.fetchall()
            return render_template('admin.html',courselist=courselist)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
            

@app.route('/manageusers')
def manageusers():
    """
    This function is used to manageusers in admin side.
    
    This manageusers function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it create a connection with mysql database and retrieve the userid and email of the users
    and render it with manage_users html template.

    Returns
    -------
    TYPE
        html : It returns the manage_users.html file.

    """
    if 'loggedin' in session:
        if session['is_admin'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT userid, email FROM users")
            userslist = cursor.fetchall()
            return render_template('manage_users.html',userslist=userslist)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
        
    

@app.route('/deleteuser/<int:id>',methods=['POST','GET'])
def deleteuser(id):
    """
    This function is used to deleteusers in admin side.
    
    This deleteusers function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it create a connection with mysql database and delete the respective user using userid
    and redirects to the adminpage.
    
    Parameters
    ----------
    TYPE
        id (int) : User id of the user.

    Returns
    -------
    TYPE
        html : It returns the manage_users.html file.

    """

    if 'loggedin' in session:
        if session['is_admin'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM users WHERE userid = %s",[id])
            mysql.connection.commit()
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
    
@app.route('/createcourse',methods=['POST','GET'])
def createcourse():
    """
    This function is used to createcourse in admin side.
    
    This createcourse function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it will check whether the request method is POST or not.
    If it is a POST request, it will create a connection with mysql databaseit and save all the values into the database from the form
    and redirects to the adminpage.
    
    
    Returns
    -------
    TYPE
        html : It returns the createcourse.html file.

    """
    if 'loggedin' in session:
        if session.get('is_admin') == 1:
            if request.method =='POST':
                deptid = request.form['deptid']
                deptname = request.form['deptname']
                totalseats = request.form['totalseats']
                intake = request.form['intake']
                freeseats = int(totalseats) - int(intake)
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO seat_availability VALUES (%s, %s, %s, %s, %s)",[deptid,deptname,totalseats,intake,freeseats])
                mysql.connection.commit()
                return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    
    return render_template('createcourse.html')

@app.route('/updatecourse/<id>',methods=['POST','GET'])
def updatecourse(id):
    """
    This function is used to updatecourse in admin side.
    
    This updatecourse function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it will check whether the request method is POST or not.
    If it is a POST request, it will create a connection with mysql database and 
    update the values in the database using department id from the values in the form and redirects to the adminpage.
    
    Parameters
    ----------
    TYPE
        id (str) : department id of the department.
    
    Returns
    -------
    TYPE
        html : It returns the updatecourse.html file.

    """
    if 'loggedin' in session:
        if session['is_admin'] == 1:
            if request.method =='POST':
                deptid = request.form['deptid']
                deptname = request.form['deptname']
                totalseats = request.form['totalseats']
                intake = request.form['intake']
                freeseats = int(totalseats) - int(intake)
                print(freeseats)
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "UPDATE seat_availability SET dept_id = %s, deptname = %s, totalseats = %s, intake = %s, freeseats = %s WHERE dept_id = %s",
                    [deptid, deptname, totalseats, intake, freeseats, id]
                    )
                mysql.connection.commit()
                return redirect(url_for('admin'))
            
            # render seat availability details from database with html template using Jinja2 
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM seat_availability WHERE dept_id = %s",[id])
            course = cursor.fetchone()
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
    
    return render_template('updatecourse.html',course=course)

@app.route('/deletecourse/<id>',methods=['POST','GET'])
def deletecourse(id):
    """
    This function is used to deletecourse in admin side.
    
    This deletecourse function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it will create a connection with mysql database and delete the respective department using department id
    and redirects to the adminpage.
    
    Parameters
    ----------
    TYPE
        id (str) : department id of the department.
    
    Returns
    -------
    TYPE
        html : It return redirect to admin.html.

    """
    if 'loggedin' in session:
        if session['is_admin'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM seat_availability WHERE dept_id = %s",[id])
            mysql.connection.commit()
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
    
@app.route('/displaycourse')
def displaycourse():
    """
    This function is used to displaycourse in admin side.
    
    This displaycourse function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it will create a connection with mysql database and fetch the department id and department name details from the database
    and render with the display_course html template else redirects the user to the adminpage.
    
    Returns
    -------
    TYPE
        html : It returns the displaycourse.html file.

    """
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT dept_id, deptname FROM seat_availability")
            course_list = cursor.fetchall()
            return render_template('display_course.html',course_list=course_list)
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin.html'))
            


@app.route('/create_enquiry',methods=['GET','POST'])
def createenquiry():
    """
    This function allows the user to create enquiry about the course that the user wants.
    
    This createenquiry function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it will check whether the request method is POST or not else redirect to the adminpage.
    If it is a POST request, it will create a connection with mysql database and save all the values into the database from the create enquiry form and 
    again create a connection with mysql database and 
    add current enquiry number, user id, date of enquiry, department id of the department that the user enquired values into the enquiry table in the database and 
    again create a connection with mysql database and fetch free seats details from the database for the department enquired by the user.
    If the free seats value is greater than zero, it wil redirect to seat_availability html page else it will redirect to seat_not_availability html page.
    
    
    
    Returns
    -------
    TYPE
        html : It returns the createenquiry.html file.

    """
    yesno = None
    message = None
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            if request.method == 'POST':
                userid = session['user_id']
                sname = request.form['sname']
                dob = request.form['dob']
                fname = request.form['fname']
                mname = request.form['mname']
                schlname = request.form['schlname']
                tenthboard = request.form['10thboard']
                tenthpercent = request.form['10thpercent']
                twelvethboard = request.form['12thboard']
                twelvethpercent = request.form['12thpercent']
                twelvethcutoff = request.form['12thcutoff']
                caste = request.form['caste']
                community = request.form['community']
                annualincome = request.form['annualincome']
                quota = request.form['quota']
                if request.form['yesno'] == 'Yes':
                    yesno = 1
                    sisbro_name = request.form['sisbroname']
                    sisbro = request.form['sisbrodept']
                else:
                    yesno = 0
                    sisbro_name = None
                    sisbro = None
                dept = request.form['dept']
                
                # initializing global variables to use in other functions as well
                global department_id,department_name
                department_id = dept
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT deptname FROM seat_availability WHERE dept_id = %s",[dept])
                department_name = cursor.fetchone()[0]
                
                
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM enquiry WHERE user_id = %s AND dept_id = %s",[userid,dept])
                dept_already_available = cursor.fetchall()
                
                # check whether the user already enquired the course or not
                if dept_already_available:
                    message = "You already enquired this course. Please check your enquiry details section."
                else:
                    # adding values to the userdetails table
                    cursor = mysql.connection.cursor()
                    cursor.execute(
                        "INSERT INTO userdetails(user_id,sname,dob,fathername,mothername,schoolname,10th_board,10th_percentage,12th_board,12th_percentage,12th_cutoff,caste,community,annual_income,quota,sis_bro_studying,sis_bro_name,sis_bro_dept,dept_asking_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [userid,sname,dob,fname,mname,schlname,tenthboard,tenthpercent,twelvethboard,twelvethpercent,twelvethcutoff,caste,community,annualincome,quota,yesno,sisbro_name,sisbro,dept]
                        )
                    mysql.connection.commit()
                
                # adding values to enquiry table
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT application_no FROM userdetails WHERE dept_asking_id = %s AND user_id = %s",[dept,userid])
                enquiry_no = cursor.fetchone()[0]
                date = datetime.now().date()
                
                # initializing global variable to use the value stored in the global variable in other functions.
                global app_no
                app_no = enquiry_no
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "INSERT INTO enquiry (enquiry_no, user_id, date, dept_id) VALUES (%s, %s, %s, %s)",
                    [enquiry_no, userid, date, dept]
                    )
                mysql.connection.commit()
                
                # checking whether the seat is available or not for the department enquired by the user
                cursor =mysql.connection.cursor()
                cursor.execute("SELECT freeseats FROM seat_availability WHERE dept_id = %s",[dept])
                freeseats = cursor.fetchone()[0]
                if freeseats >0:
                    return redirect(url_for('seat_available',app_no=app_no))
                else:
                    return redirect(url_for('seat_not_available'))
                
            # fetching the department id and department name details and render with the html template using Jinja2
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT dept_id, deptname FROM seat_availability")
            departments = cursor.fetchall()
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin'))
    
    
    return render_template("createenquiry.html",departments=departments,message=message)

@app.route('/seat_available/<int:app_no>',methods = ['GET','POST'])
def seat_available(app_no):
    """
    This function is used to confirm that the seat is available.
    
    This seat available function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it will check whether the request method is POST or not else redirect to the adminpage.
    If it is a POST request, create a connection with mysql database and update the seat locked value to 1 in the enquiry table 
    from the database and send a email to the user regarding the confirmation of the seat.
    Automatically update the intake and free seats values in the seat availability table from the database and
    redirect the user to the homepage.
    
    Returns
    -------
    TYPE
        html : It returns the seat_availbility.html file.

    """
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            if request.method == 'POST':
                userid = session['user_id']
                email = session['email']
                # initializing global variables to use in other functions as well
                global department_id,department_name
                seat_locked = 1
                
                # update the seat lock value to 1 in enquiry table in the database
                cursor = mysql.connection.cursor()
                cursor.execute("UPDATE enquiry SET seat_locked = %s WHERE enquiry_no = %s AND user_id = %s",[seat_locked,app_no,userid])
                mysql.connection.commit()
                
                # send confirmation email to the user regarding seat confirmation
                '''msg = Message(f'Seat Locked Successfull for the department - {department_name} you enquired',sender=config.email,
                recipients=[email]
                )
                msg.body = f'
                Dear student, the seat has been locked for the department {department_name} you have enquired.
                Please visit the college for further process. Thankyou.
                '
                mail.send(msg)'''
                
                # fetching intake and free seats details from seat_availability table in the database for the department enquired by the user
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT intake, freeseats FROM seat_availability WHERE dept_id =%s",[department_id])
                seat_details = cursor.fetchone()
                intake = seat_details[0]
                freeseats=seat_details[1]
                
                # update intake and freeseats details in seat_availability table in the database
                cursor = mysql.connection.cursor()
                cursor.execute("UPDATE seat_availability SET intake = %s, freeseats = %s WHERE dept_id = %s",[intake+1,freeseats-1,department_id])
                mysql.connection.commit()
                return redirect(url_for('home'))
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin'))
                
    return render_template('seat_available.html')

@app.route('/seat_not_available',methods = ['GET','POST'])
def seat_not_available():
    """
    This function is used to tell that the seat looking by the user is not available.
    
    This seat available function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it returns seat not available template to the user else return to the admin page.
    
    Returns
    -------
    TYPE
        html : It returns the seat_not_availbility.html file.

    """
    if 'loggedin' in session:
        print(session.get('is_admin'))
        if session.get('is_admin') == None:
            return render_template("seat_not_available.html")
        return redirect(url_for('signin'))
    return redirect(url_for('signin'))

@app.route('/display_enquiry/')
def display_enquiry():
    """
    This function is used to display enquiry details.
    
    This display_enquiry function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it will create a connection with mysql database and fetch the all the enquiry details for the respective user using user id from the database
    and render with the display_enquiry html template else redirects the user to the adminpage.
    
    Returns
    -------
    TYPE
        html : It returns the display_enquiry.html file.

    """
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            user_id = session['user_id']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM enquiry WHERE user_id = %s",[user_id])
            enquiry_details = cursor.fetchall()
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin'))
            
    return render_template('display_enquiry.html',enquiry_details = enquiry_details)


@app.route('/manageenquiry')
def manageenquiry():
    """
    This function is used to manage enquiries in admin side.
    
    This manageusers function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it create a connection with mysql database and retrieve all the enquiry details from the enquiry 
    table and render it with manageenquiry html template.

    Returns
    -------
    TYPE
        html : It returns the manageenquiry.html file.

    """
    if 'loggedin' in session:
       if session['is_admin'] == 1:
           cursor = mysql.connection.cursor()
           cursor.execute("SELECT * FROM enquiry")
           enquiry_details = cursor.fetchall()
           
           return render_template('manageenquiry.html',enquiry_details = enquiry_details)
        
@app.route('/updateenquiry/<int:id>',methods=['POST','GET'])
def updateenquiry(id):
    """
    This function is used to updateenquiry in admin side.
    
    This updateenquiry function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it will check whether the request method is POST or not.
    If it is a POST request, it will create a connection with mysql database and 
    update the values in the enquiry table from the database using enquiry number from form
    and automatically update the intake and freeseats values in seat_availability table from the database and redirects to the adminpage.
    
    Parameters
    ----------
    TYPE
        id (int) : enquiry number of the user enquiry application.
    
    Returns
    -------
    TYPE
        html : It returns the updateenquiry.html file.

    """

    if 'loggedin' in session:
        if session['is_admin'] == 1:
            if request.method =='POST':
                enquiry_no = request.form['enquiry_no']
                user_id = request.form['user_id']
                date = request.form['date']
                dept_id = request.form['dept_id']
                seat_locked = request.form['seat_locked']
                
                #update enquiry details in enquiry table
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "UPDATE enquiry SET enquiry_no = %s, user_id = %s, date = %s, dept_id = %s, seat_locked = %s WHERE enquiry_no = %s",
                    [enquiry_no, user_id, date, dept_id, seat_locked, id]
                    )
                mysql.connection.commit()
                
                # fetching intake and freeseats details from seat_availability table in the database
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT intake, freeseats FROM seat_availability WHERE dept_id =%s",[dept_id])
                seat_details = cursor.fetchone()
                intake = seat_details[0]
                freeseats=seat_details[1]
                if seat_locked == 1:
                    cursor = mysql.connection.cursor()
                    cursor.execute("UPDATE seat_availability SET intake = %s, freeseats = %s WHERE dept_id = %s",[intake+1,freeseats-1,dept_id])
                    mysql.connection.commit()
                else:
                    cursor = mysql.connection.cursor()
                    cursor.execute("UPDATE seat_availability SET intake = %s, freeseats = %s WHERE dept_id = %s",[intake-1,freeseats+1,dept_id])
                    mysql.connection.commit()
                return redirect(url_for('admin'))
            
            # rendering enquiry details from the databse to the html template using Jinja2
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM enquiry WHERE enquiry_no = %s",[id])
            enquiry_details = cursor.fetchone()
            print(enquiry_details)
            return render_template('updateenquiry.html',enquiry_details=enquiry_details)
            
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
    
    return render_template('updateenquiry.html',enquiry_details=enquiry_details)


@app.route('/deleteenquiry/<int:id>',methods=['POST','GET'])
def deleteenquiry(id):
    """
    This function is used to delete enquiry details in admin side.
    
    This deleteenquiry function checks whether the user is loggedin. 
    If it is true, it checks whether the user is an admin else it redirects the user to the signin page.
    If it is also true, it create a connection with mysql database and delete the enquiry details using enquiry number
    and redirects to the adminpage.
    
    Parameters
    ----------
    TYPE
        id (int) : enquiry number of user enquiry application.
    
    Returns
    -------
    TYPE
        html : html : It returns redirect to admin.html.

    """
    if 'loggedin' in session:
        if session['is_admin'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM enquiry WHERE enquiry_no = %s",[id])
            mysql.connection.commit()
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))
    
@app.route('/contact')
def contact():
    """
    This function is used to display the contact information of the college.
    
    This contact function checks whether the user is loggedin. 
    If it is true, it checks whether the user is not an admin else it redirects the user to the signin page.
    If it is also true, it returns contact html template to the user else return to the admin page.
    
    Returns
    -------
    TYPE
        html : It returns the contact.html file.

    """
    if 'loggedin' in session:
        if session.get('is_admin') == None:
            return render_template('contact.html')
        else:
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('signin'))

@app.route('/announcement', methods=['GET', 'POST'])
def announcement():
    if request.method == 'POST':
        content = request.form['content']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO notifications (content) VALUES (%s)", (content,))
        mysql.connection.commit()
        return 'Announcement added successfully'
    return render_template('ann.html')
@app.route('/getnotify')
def getnotify():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM notifications")
    announcements = cursor.fetchall()
    return render_template('annoumncement.html', announcements=announcements)


if __name__=='__main__':
    app.run(debug=True,use_reloader=True)



