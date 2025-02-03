from flask import render_template, request, redirect, url_for, Blueprint, session, current_app
from .blueprints.student import Student


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # secret_key = current_app.config['SECRET_KEY']  # Access secret key
    # print("Secret Key:", secret_key)  # Just for testing, remove in production
    return render_template('index.html')

@main.route('/loginregister')
def loginregister():
    return render_template('loginregister.html')

@main.route('/registerstudent',methods=['POST'])
def registerstudent():
    idno:str = request.form['idno']
    fullname:str = request.form['fullname']
    course:str = request.form['course']
    year:int = request.form['year']

    session['student'] = {
        'idno': idno,
        'fullname': fullname,
        'course': course,
        'year': year
    }

    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
def dashboard():
    student_data = session.get('student')
    student = Student(
        idno= student_data['idno'],
        fullname = student_data['fullname'],
        course = student_data['course'],
        year = student_data['year'],
    )
    print(student)
    return render_template('dashboard.html', student=student)

