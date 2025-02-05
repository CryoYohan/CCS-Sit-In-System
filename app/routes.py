from flask import render_template, request, redirect, url_for, Blueprint, session, abort
from .modules.user_mgt_module.student import Student
from .modules.login_register_module import Authorization

# Register as a Blueprint for create_app() function to recognize as Flask app
main = Blueprint('main', __name__)

# Initialize Authorization instance Login Register Module
auth = Authorization()


@main.route('/')
def index():
    """Landing page."""
    return render_template('index.html')

@main.route('/login')
def login():
    """Login page."""
    return render_template('login.html')


@main.route('/dashboard')
def dashboard():
    """Dashboard page."""
    if not session['student'] == None:
        student_data = session.get('student')
        student = Student(
                            idno= student_data['idno'],
                            fullname = student_data['fullname'],
                            course = student_data['course'],
                            year = student_data['year'],
             )
        print(student)
        return render_template('dashboard.html', student=student)
    else:
        abort(403)

@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@main.route('/logout')
def logout():
    """Logout page."""
    session['student'] = None
    return redirect(url_for('main.index'))

@main.route('/loginstudent', methods=['POST'])
def loginstudent():
    """Login a student."""
    idno:str = request.form['idno']
    password:str = request.form['password']

    # Use Login Register Module for authorization
    if auth.student_account_exist_and_correct_credentials(idno=idno,password=password):
        return redirect(url_for('main.dashboard'))     
    else:
        return redirect(url_for('main.login'))

@main.route('/registerstudent',methods=['POST'])
def registerstudent():
    """Register a student"""
    idno:str = request.form['idno']
    fullname:str = request.form['fullname']
    course:str = request.form['course']
    year:int = request.form['year']
    email:str = request.form['email']
    password:str = request.form['password']

    # Use Login Register Module for student registration
    if auth.student_is_registered(idno=idno,
                                  fullname=fullname,
                                  course=course,
                                  year=year,
                                  email=email,
                                  password=password
                                  ):
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('main.login'))