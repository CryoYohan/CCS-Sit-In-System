from flask import render_template, request, redirect, url_for, Blueprint, session, abort,jsonify, flash
from .modules.user_mgt_module.student import Student
from .modules.login_register_module import Authorization

# Register as a Blueprint for create_app() function to recognize as Flask app
main = Blueprint('main', __name__)

# Initialize Authorization instance Login Register Module
auth = Authorization()


@main.route('/')
def index():
    """Landing page."""
    return render_template('index.html', user_in_login_page=False)

@main.route('/login')
def login():
    """Login page."""
    return render_template('login.html',user_in_login_page=True)


@main.route('/dashboard')
def dashboard():
    """Dashboard page."""
    try:
        if not session['student'] == None:
            student_data = session.get('student')
            student = Student(
                                idno= student_data['idno'],
                                firstname = student_data['firstname'],
                                middlename = student_data['middlename'],
                                lastname =student_data['lastname'],
                                course = student_data['course'],
                                year = student_data['year'],
                                email = student_data['email'],
                )
            print(student)
            return render_template('dashboard.html', student=student, )
        else:
            return redirect(url_for('main.login'))
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))

@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@main.route('/logout')
def logout():
    """Logout page."""
    session['student'] = None
    message = "You have been logged out."
    flash(message, 'success')
    return redirect(url_for('main.index'))

@main.route('/loginstudent', methods=['POST'])
def loginstudent():
    """Login a student."""
    idno: str = request.form['idno']
    password: str = request.form['password']

    # Use Login Register Module for authorization
    if auth.user_account_exist_and_correct_credentials(idno=idno, password=password):
        # If login is successful, send a message to show SweetAlert before redirecting
        flash("Login successful.", 'success')
        return redirect(url_for('main.dashboard'))
    else:
        # If login fails, pass error message to be used with SweetAlert
        login_error = "Invalid credentials. Please try again."
        message = "Invalid credentials. Please try again."
        flash(message, 'error')
        return render_template('login.html', user_in_login_page=True)



@main.route('/registerstudent', methods=['POST'])
def registerstudent():
    """Register a student"""
    idno:str = request.form['idno']
    firstname:str = request.form['firstname']
    middlename:str = request.form['middlename']
    lastname:str = request.form['lastname']
    course:str = request.form['course']
    year:int = request.form['year']
    email:str = request.form['email']
    password:str = request.form['password']

    # Use Login Register Module for student registration
    registration_success = auth.user_is_registered(idno=idno,
                                                   firstname=firstname,
                                                   middlename=middlename,
                                                   lastname=lastname,
                                                   course=course,
                                                   year=year,
                                                   email=email,
                                                   password=password)
    if registration_success:
        # If registration is successful, show a success alert and redirect to login page
        message = "Registration successful. Please login."
        flash(message, 'success')
        return redirect(url_for('main.login'))
    else:
        # If registration failed, show an error alert
        return redirect(url_for('main.login'))
