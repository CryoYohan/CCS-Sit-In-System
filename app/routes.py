from flask import render_template, request, redirect, url_for, Blueprint, session, flash, current_app
from .modules.user_mgt_module.student import Student
from .modules.login_register_module import Authorization
from .modules.reservation_module.reserve_lab import Reservation
from datetime import datetime
import os
from werkzeug.utils import secure_filename


# Register as a Blueprint for create_app() function to recognize as Flask app
main = Blueprint('main', __name__, template_folder='templates/student')

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize Authorization instance Login Register Module
auth = Authorization()

# Initialize Reservation instance
reservation = Reservation()

student = None # Global student object to be reusable

# Function to check if the file extension is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@main.route('/')
def index():
    """Landing page."""
    return render_template(
                            'index.html',
                            user_in_login_page=False, 
                            action='Login'
                            )

@main.route('/login')
def login():
    """Login page."""
    return render_template(
                            'login.html',
                            user_in_login_page=True,
                            action='Back'
                           )


@main.route('/dashboard')
def dashboard():
    """Dashboard page."""
    global student
    try:

        if session.get('student') is not None:
            if student is None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template(
                                    'dashboard.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout',
                                   )
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))


@main.route('/announcements')
def announcements():
    """Announcements page."""
    global student
    try:

        if session.get('student') is not None:
            if student is None:
                student_data = session.get('student')
                student = Student(**student_data)
                
            response = student.retrieve_all_announcements()
            print(announcements)
            return render_template(
                                    'announcements.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout',
                                    announcements=response['announcements'],
                                   )
         
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
    """Render Sit-in page."""
    global student
    labs = reservation.retrieve_labs()
    datenow = datetime.now()

    if not session.get('student') == None:
        if not student:
            student_data = session.get('student')
            student = Student(**student_data)

        return render_template(
                                'sitin.html', 
                                student=student,
                                user_in_login_page=True,
                                action='Logout',
                                labs=labs,
                                datenow=datenow
                               )
    else:
        message = "Please login first."
        flash(message)
        return redirect(url_for('main.login'))


@main.route('/reserve')
def reserve():
    """Reserve page."""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            
            labs = reservation.retrieve_labs()

            return render_template(
                                    'reserve.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout',
                                    labs=labs,
                                   )
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        #session['student'] = None
        return redirect(url_for('main.login'))
    
@main.route('/records')
def records():
    """Record History Page"""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)
            
            records = reservation.retrieve_sitinrecords(idno=student.idno)

            return render_template('records.html', student=student,user_in_login_page=True,action='Logout', records=records)

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

            records = reservation.retrieve_sessionhistory(idno=student.idno)

            return render_template('sessions.html', student=student,user_in_login_page=True,action='Logout', records=records)

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
            return render_template(
                                    'rulesregulations.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout'
                                   )
         
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
            
            profileicons = student.profileicons

            return render_template(
                                    'profilesettings.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout',
                                    profileicons=profileicons,
                                    )
         
        else:
            message = "Please login first."
            flash(message)
            return redirect(url_for('main.login'))
        
    except Exception as e:
        flash(str(e),'error')
        flash("Please try again")
        return redirect(url_for('main.login'))      

@main.route('/logout')
def logout():
    """Logout page."""
    global student
    session['student'] = None
    student = None
    message = "You have been logged out."
    flash(message, 'success')
    return redirect(url_for('main.login'))


@main.route('/sitin_lab', methods=['POST'])
def sitin_lab():
    """Handles POST method in sit-in functionality"""
    global student
    try:
        lab = request.form['lab']
        reason = request.form['reason']
        date = request.form['date']
        print(lab, reason, date)
        
        response = reservation.add_sitin_details(
                                                lab_id=reservation.retrieve_lab_id(lab), 
                                                idno=student.idno, reason=reason,
                                                )
        
        if response['success']:
            flash('Request Sent!', 'success')
            return redirect(url_for('main.sitin'))

        else:
            flash(response['error'],'error')
            return redirect(url_for('main.sitin'))
    except Exception as e:
        flash(str(e),'error')
        return redirect(url_for('main.sitin'))

@main.route('/uploadprofile', methods=['POST'])
def uploadprofile():
    """Upload Profile Picture Route"""
    global student
    if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)

    filenamefromicon = request.form['profile_icon2'] # Extract default icon selection


    print(f'Filename from icon: {filenamefromicon}')
    print("Request files:", request.files)  # Debugging: Print received files

    profile_picture_uploaded = 'profile_picture' in request.files
    print(f'Profile picture uploaded: {profile_picture_uploaded}')

    if profile_picture_uploaded and not filenamefromicon: 

        file = request.files['profile_picture']

        if file.filename == '':
            flash("No selected file")
            return redirect(url_for('main.profilesettings'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure filename

            upload_folder = os.path.abspath(os.path.join(current_app.root_path, "static/images/profileicons"))
            filepath = os.path.join(upload_folder, filename)

            # 🔥 FIX: Don't create a new folder—only check if it exists!
            if not os.path.isdir(upload_folder):
                print(f"⚠️ ERROR: Directory {upload_folder} does NOT exist!")
                flash("Upload folder missing. Contact admin.", "danger")
                return redirect(url_for('main.profilesettings'))

            print(f"Saving file to: {filepath}")  # Debugging line
            file.save(filepath.replace("\\", "/"))  # Fix Windows backslash issue

            if os.path.exists(filepath):  # Verify if the file was actually saved
                print("✅ File successfully saved!")
            else:
                print("❌ File was NOT saved!")

            
            response = student.upload_profile_icon(profile_icon=filename, student=student)

            if response['success']:
                flash("Profile picture uploaded successfully!", "success")
                student = response['student'] # reload new student object with new image
                session['student'] = student.__dict__ # reload new student session with new image from new student object
                return redirect(url_for('main.profilesettings'))
            else:
                flash(response['error'], "error")
                return redirect(url_for('main.profilesettings'))

    elif filenamefromicon and profile_picture_uploaded:
        response = student.upload_profile_icon(profile_icon=filenamefromicon, student=student)

        if response['success']:
            flash("Profile picture uploaded successfully2!", "success")
            student = response['student']
            session['student'] = student.__dict__ # reload new student session with new image from new student object
            return redirect(url_for('main.profilesettings'))
        else:
            flash(response['error'], "error")
            return redirect(url_for('main.profilesettings'))
    else:
        flash("Please select a profile picture or upload one.", "error")
        return redirect(url_for('main.profilesettings'))




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
    response = auth.user_account_exist_and_correct_credentials(idno=idno, password=password,url='student')
    if response['success']:
        del response['success']
        session['student'] = response
        flash("Login successful.", 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash(response['error'], 'error')
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
    student = Student(
                    idno=idno,
                    firstname=firstname,
                    middlename=middlename,
                    lastname=lastname,
                    course=course,
                    year=year,
                    email=email,
                    image=None,
                    session=None,
                    )
    response = auth.user_is_registered(
                                **student.__dict__,
                                password=password,
                                url='student'
                                )
    
    if response['success']:
        # If registration is successful, show a success alert and redirect to login page
        del response['success']
        print(response)
        session['student'] = response
        message = "Registration successful. Please login."
        flash(message, 'success')
        return redirect(url_for('main.login'))
    else:
        # If registration failed, show an error alert
        flash(response['error'], 'error')
        return redirect(url_for('main.login'))
