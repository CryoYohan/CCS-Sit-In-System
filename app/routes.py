from flask import render_template, request, redirect, url_for, Blueprint, session, abort,jsonify, flash
from .modules.user_mgt_module.student import Student
from .modules.login_register_module import Authorization

# Register as a Blueprint for create_app() function to recognize as Flask app
main = Blueprint('main', __name__, template_folder='templates/student')

# Initialize Authorization instance Login Register Module
auth = Authorization()

student = None # Global student object to be reusable
@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@main.route('/')
def index():
    """Landing page."""
    return render_template('index.html', user_in_login_page=False, action='Login', is_admin=False)

@main.route('/login')
def login():
    """Login page."""
    return render_template('login.html',user_in_login_page=True,action='Back',is_admin=False)


@main.route('/dashboard')
def dashboard():
    """Dashboard page."""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template('dashboard.html', student=student,user_in_login_page=True,action='Logout',is_admin=False)
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))

@main.route('/sitin')
def sitin():
    """Profile page."""
    labs = [
        {
        'name': 'Lab 530',
        'description': 'A lab for 530',
        'image': '530.jpg',
        },
        {
        'name': 'Lab 544',
        'description': 'A lab for 544',
        'image': '544.avif',
        },
        {
        'name': 'Lab 526',
        'description': 'A lab for 526',
        'image': '526.jpg',
        },
        {
        'name': 'Lab 524',
        'description': 'A lab for 524',
        'image': '524.jpg',
        },
    ]
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template('sitin.html', student=student,user_in_login_page=True,action='Logout',is_admin=False)
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))

@main.route('/sessions')
def sessions():
    """Remaining Sessions Page"""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template('sessions.html', student=student,user_in_login_page=True,action='Logout',is_admin=False)

        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))


@main.route('/rulesregulations')
def rulesregulations():
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template('rulesregulations.html', student=student,user_in_login_page=True,action='Logout',is_admin=False)
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))


@main.route('/profilesettings')
def profilesettings():
    """Profile page."""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template('profilesettings.html', student=student,user_in_login_page=True,action='Logout',is_admin=False)
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    """Logout page."""
    session['student'] = None
    message = "You have been logged out."
    flash(message, 'success')
    return redirect(url_for('main.index'))


@main.route('/reserve_lab', methods=['POST'])
def reserve_lab():
    pass


@main.route('/editprofile', methods=['POST'])
def editprofile():
    """Edit Profile Route"""
    global student
    form_data = request.form.to_dict()

    # Get and validate password fields
    password = form_data.pop('editpassword', None) # Remove from form_data dict
    confirmpassword = form_data.pop('editconfirmpassword', None)

    if password and password != confirmpassword:
        flash("Passwords do not match!", "error")
        return redirect(url_for("main.profilesettings"))

    # Create update dictionary with only non-empty fields
    edit_data = {
                "idno": student.idno,  # Keep ID in case it's required
                "firstname": form_data.get("editfirstname") or student.firstname,
                "middlename": form_data.get("editmiddlename") or student.middlename,
                "lastname": form_data.get("editlastname") or student.lastname,
                "course": form_data.get("editcourse") or student.course,
                "year": form_data.get("edityear") or student.year,
                "email": form_data.get("editemail") or student.email
                }

    # Update password only if provided
    if password:
        hashed_password = auth.hashpasword.hashpassword(password)
        edit_data["password"] = hashed_password  # Add hashed password to update fields

    try:
        if edit_data:
            #  Update the student record once (optimized)
            student.edit(**edit_data)

            #  Update session with non-sensitive fields (exclude password)
            session["student"] = {k: v for k, v in edit_data.items() if k != "password"}

            #  Update the global `student` object with new data
            student.firstname = edit_data["firstname"]
            student.middlename = edit_data["middlename"]
            student.lastname = edit_data["lastname"]
            student.course = edit_data["course"]
            student.year = edit_data["year"]
            student.email = edit_data["email"]

            flash("Profile updated successfully!", "success")
        else:
            flash("No changes made.","info")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.profilesettings"))


@main.route('/loginstudent', methods=['POST'])
def loginstudent():
    global student
    """Login a student."""
    idno: str = request.form['idno']
    password: str = request.form['password']

    # Use Login Register Module for authorization
    student_sucessfully_login = auth.user_account_exist_and_correct_credentials(idno=idno, password=password)
    if student_sucessfully_login:
        session['student'] = student_sucessfully_login.__dict__
        student = student_sucessfully_login
        flash("Login successful.", 'success')
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('login.html', user_in_login_page=True,action='Back')



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
    student_sucessfully_registered = auth.user_is_registered(idno=idno,
                                firstname=firstname,
                                middlename=middlename,
                                lastname=lastname,
                                course=course,
                                year=year,
                                email=email,
                                password=password)
    
    if student_sucessfully_registered:
        # If registration is successful, show a success alert and redirect to login page
        session['student'] = student_sucessfully_registered.__dict__
        message = "Registration successful. Please login."
        flash(message, 'success')
        return redirect(url_for('main.login'))
    else:
        # If registration failed, show an error alert
        return redirect(url_for('main.login'))
