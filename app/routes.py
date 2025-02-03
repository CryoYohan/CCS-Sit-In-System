from flask import render_template, request, redirect, url_for, Blueprint, session, abort
from .blueprints.student import Student
from .database.dbhelper import Databasehelper
from .blueprints.hashpw import PasswordHashing

main = Blueprint('main', __name__)
hashpasword = PasswordHashing()
db = Databasehelper()


@main.route('/')
def index():
    """Landing page."""
    # secret_key = current_app.config['SECRET_KEY']  # Access secret key
    # print("Secret Key:", secret_key)  # Just for testing, remove in production
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
    idno:str = request.form['idno']
    password:str = request.form['password']
    student_exists = db.find_record('student',idno)
    if student_exists:
        for data in student_exists:
            if data['password'] == password:
                session['student'] = {
                    'idno': data['idno'],
                    'fullname': data['fullname'],
                    'course': data['course'],
                    'year': data['year']
                }
                return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('main.login'))

@main.route('/registerstudent',methods=['POST'])
def registerstudent():
    idno:str = request.form['idno']
    fullname:str = request.form['fullname']
    course:str = request.form['course']
    year:int = request.form['year']
    email:str = request.form['email']
    password:str = request.form['password']
    hashed_password = hashpasword.hashpassword(password)

    db.add_record('student',idno=idno,fullname=fullname,course=course,year=year,email=email,password=hashed_password)

    session['student'] = {
        'idno': idno,
        'fullname': fullname,
        'course': course,
        'year': year
    }

    return redirect(url_for('main.dashboard'))