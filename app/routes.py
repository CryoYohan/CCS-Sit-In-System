from flask import render_template, request, redirect, url_for, Blueprint, session, flash, current_app, jsonify
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
    
@main.route('/leaderboards')
def leaderboards():
    """Render leaderboards"""
    """Dashboard page."""
    global student
    try:
        update_date = datetime.today().strftime('%B %d, %Y')

        if session.get('student') is not None:
            if student is None:
                student_data = session.get('student')
                student = Student(**student_data)
            return render_template(
                                    'leaderboards.html', 
                                    student=student,
                                    user_in_login_page=True,
                                    action='Logout',
                                    update_date= update_date
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
            
            records = reservation.retrieve_sitinrecords()

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

@main.route('/resources')
def resources():
    """Resources Page"""
    global student
    try:

        if not session['student'] == None:
            if student == None:
                student_data = session.get('student')
                student = Student(**student_data)

            return render_template('resources.html', student=student,
                                   user_in_login_page=True,
                                   action='Logout')

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

            return render_template('sessions.html', student=student,
                                   user_in_login_page=True,
                                   action='Logout')

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
    if session.get('student') and student is None:
        student_data = session.get('student')
        student = Student(**student_data)

    filenamefromicon = request.form.get('profile_icon2', '')  # Default icon selection
    uploaded_file = request.files.get('profile_picture')      # Uploaded file

    print(f'Filename from icon: {filenamefromicon}')
    print("Request files:", request.files)
    print(f'Profile picture uploaded: {bool(uploaded_file and uploaded_file.filename)}')

    profileicons = ['bear.png', 'cat.png', 'chicken.png', 'meerkat.png',
                    'panda.png', 'polar-bear.png', 'shark.png', 'weasel.png', 'wolf.png']

    # CASE 1: Uploading a new custom picture
    if uploaded_file and uploaded_file.filename and not filenamefromicon:
        if allowed_file(uploaded_file.filename):
            # Delete old uploaded picture if not a default icon
            if student.image and student.image not in profileicons:
                old_image_path = os.path.join(current_app.static_folder, 'images', 'profileicons', student.image)
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                        print(f"Deleted old profile picture: {old_image_path}")
                    except Exception as e:
                        print(f"Error deleting old profile picture: {str(e)}")

            # Save new file
            filename = secure_filename(uploaded_file.filename)
            upload_folder = os.path.abspath(os.path.join(current_app.root_path, "static/images/profileicons"))
            filepath = os.path.join(upload_folder, filename)

            if not os.path.isdir(upload_folder):
                flash("Upload folder missing. Contact admin.", "danger")
                return redirect(url_for('main.profilesettings'))

            uploaded_file.save(filepath.replace("\\", "/"))

            if os.path.exists(filepath):
                print("✅ File successfully saved!")
            else:
                print("❌ File was NOT saved!")

            response = student.upload_profile_icon(profile_icon=filename, student=student)

            if response['success']:
                flash("Profile picture uploaded successfully!", "success")
                student = response['student']
                session['student'] = student.__dict__
                return redirect(url_for('main.profilesettings'))
            else:
                flash(response['error'], "error")
                return redirect(url_for('main.profilesettings'))

        else:
            flash("Invalid file type.", "error")
            return redirect(url_for('main.profilesettings'))

    # CASE 2: Selecting a default icon only
    elif filenamefromicon:
        # Delete old uploaded picture if not a default icon
        if student.image and student.image not in profileicons:
            old_image_path = os.path.join(current_app.static_folder, 'images', 'profileicons', student.image)
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                    print(f"Deleted old profile picture: {old_image_path}")
                except Exception as e:
                    print(f"Error deleting old profile picture: {str(e)}")

        response = student.upload_profile_icon(profile_icon=filenamefromicon, student=student)

        if response['success']:
            flash("Profile picture changed successfully!", "success")
            student = response['student']
            session['student'] = student.__dict__
            return redirect(url_for('main.profilesettings'))
        else:
            flash(response['error'], "error")
            return redirect(url_for('main.profilesettings'))

    # CASE 3: Neither uploaded nor selected
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
    

@main.route('/api/announcements')
def get_announcements():
    """FETCH ALL ANNOUNCEMENTS"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401  # Unauthorized status code

    if student is None:
        student = Student(**session.get('student'))

    response = student.get_announcements_for_student()

    if response['success']:
        announcements = []
        for announcement in response['data']:
            announcements.append({
                'post_id': announcement['post_id'],
                'post_title': announcement['post_title'],
                'post_description': announcement['post_description'],
                'image': announcement['image'],
                'posted_by': announcement['posted_by'],
                'date_posted': announcement['date_posted'],
            })

        return jsonify({
            'success': True,
            'data': announcements
        })
    else:
        return jsonify({
            'success': False,
            'message': response['message']
        })
    
@main.route('/api/labs')
def fetch_labs():
    """FETCH ALL LABS"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401
    if student is None:
        student = Student(**session.get('student'))
    
    labs = reservation.retrieve_labs()

    json_formatted_data = [
        {
            'lab_id': lab['lab_id'],
            'lab_name': lab['lab_name'],
            'lab_description': lab['lab_description'],
            'vacant_time': lab['vacant_time'],
            'slots': lab['slots'],
            'image':lab['image'],
            'computers': lab['computers']
        }
        for lab in labs['data']
    ]

    return jsonify(
        json_formatted_data
    )
@main.route('/api/labs/<lab_id>')
def fetch_lab(lab_id):
    """FETCH ONE LAB ALONG WITH ITS SCHEDULES"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401
    if student is None:
        student = Student(**session.get('student'))
    
    labs = reservation.retrieve_one_lab(lab_id=lab_id)

    if labs['success']:
        lab = labs['data'][0]  # Directly use the single lab object
        
        # Parse the vacant times into a list
        vacant_times = lab['vacant_time'].split(',')
        vacant_times = [time.strip() for time in vacant_times]  # Remove any extra spaces
        
        return jsonify({
            'lab_id': lab['lab_id'],
            'lab_name': lab['lab_name'],
            'lab_description': lab['lab_description'],
            'vacant_time': vacant_times,  # List of available schedules
            'slots': lab['slots'],
            'image': lab['image'],
            'computers': lab['computers'],
            'success': True
        })
    else:
        return jsonify({
            'success': False,
            'message': labs['error']
        })


@main.route('/api/session-records/<idno>')
def get_session_records(idno):
    """FETCH ALL SESSION RECORDS"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401
    
    if student is None:
        student = Student(**session.get('student'))

    response = student.retrieve_student_sessions_history(idno=idno)
    if response['success']:
        print(response['data'])

        json_formatted_data = [{
            'record_id': data['record_id'],  # Add this line
            'idno': data['idno'],
            'lab_name': data['lab_name'],
            'sitin_in': data['sitin_in'],
            'sitin_out': data['sitin_out'],
            'reason': data['reason'],
            'staff_idno': data['staff_idno'],
            'logged_off_by': data['logged_off_by'],
            'status': data['status'],
        } 
            for data in response['data']
        ]
        return jsonify(json_formatted_data)
    else:
        print(response['error'])
        return jsonify({
            'success': False,
            'message': response['error']
        })


@main.route('/api/reserve-lab', methods=['POST'])
def reserve_lab():
    """API TO RESERVE LAB"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401
    
    if student is None:
        student = Student(**session.get('student'))

    # Parse JSON data from the request
    data = request.get_json()
    lab = data.get('lab')
    purpose = data.get('purpose')
    reserve_date = data.get('reserve_date')  # Expected format: "YYYY-MM-DD"
    time = data.get('time')  # Expected format: "HH:MM"
    fullDateTime = data.get('fullDateTime')  # Expected format: "YYYY-MM-DD HH:MM"
    computer = data.get('computer')

    fix_computer_index = int(computer) + 1

    # Validate required fields
    if not all([lab, purpose, reserve_date, time, fullDateTime, computer]):
        return jsonify({
            'success': False,
            'message': 'Missing required fields. Please fill out all fields.'
        }), 400

    # Combine reserve_date and time into a datetime object
    try:
        reserve_datetime = datetime.strptime(fullDateTime, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Invalid date or time format. Please use "YYYY-MM-DD HH:MM".'
        }), 400


    # Check if the reservation datetime is in the past
    current_datetime = datetime.now()
    if reserve_datetime <= current_datetime:
        return jsonify({
            'success': False,
            'message': 'Reservation date and time must be in the future.'
        }), 400

    # Prepare the reservation data
    reservation_data = {
        'idno': student.idno,  # Use the logged-in student's ID
        'lab_id': lab,
        'purpose': purpose,
        'request_date': current_datetime,  # Use the current datetime
        'reserve_date': fullDateTime,
        'status': 'Pending',
        'computer': fix_computer_index,
        'message': f'Hey {student.firstname.title()}! Your reservation request is sent. Please wait for confirmation.'
    }
    print(reservation_data)

    # Call the reservation function
    response = reservation.request_reservation(**reservation_data)

    # Return the response to the frontend
    return jsonify(response)


@main.route('/api/reservation-history')
def get_reservation_history():
    """Fetch reservation history for the logged-in student"""
    try:
        global student

        # Check if the student is logged in
        if not session.get('student'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access is prohibited.'
            }), 401

        # Initialize the student object if not already done
        if student is None:
            student = Student(**session.get('student'))

        # Fetch reservation history for the student
        response = reservation.retrieve_reservation_history(idno=student.idno)

        if not response.get('success'):
            return jsonify({
                'success': False,
                'message': response.get('message', 'Failed to fetch reservation history.')
            }), 500

        json_formatted_data = [
            {
                'reservation_id' : data['reservation_id'],
                'idno': data['idno'],
                'request_date': data['request_date'],
                'reserve_date': data['reserve_date'],
                'status':data['status'],
                'message': data['message'],
                'staff_idno': data['staff_idno'],
                'purpose': data['purpose'],
                'lab_id': data['lab_id'],
            }
            for data in response['data']
        ]

        # Return the reservation history
        return jsonify({
            'success': True,
            'data': json_formatted_data,
        })

    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_reservation_history: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An internal server error occurred.'
        }), 500

@main.route('/api/calendar-data', methods=['GET'])
def get_calendar_data():
    """Fetch calendar data for a specific year and month"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        if not year or not month:
            return jsonify({
                'success': False,
                'message': 'Year and month are required.'
            }), 400

        # Fetch calendar data from the database or another source
        calendar_data = {
            "2025-02-20": { "status": "available", "schedules": ["9am-10am", "1pm-2pm"] },
            "2025-02-19": { "status": "available", "schedules": ["9am-10am", "1pm-2pm"] },
            "2025-02-21": { "status": "full", "schedules": [] },
            "2025-02-22": { "status": "closed", "schedules": [] }
        }

        return jsonify({
            'success': True,
            'data': calendar_data,
        })
    except Exception as e:
        print("Error fetching calendar data:", str(e))
        return jsonify({
            'success': False,
            'message': 'Failed to fetch calendar data.'
        }), 500
    

@main.route('/api/cancel-reservation/<reservation_id>', methods=['GET', 'POST'])
def cancel_reservation_student(reservation_id):
    """Cancel Reservation"""
    global student
    if not session.get('student'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401

    if student is None:
        student = Student(**session.get('student'))

    if not reservation_id:
        return jsonify({
            'success': False,
            'message': 'Reservation ID is required.'
        }), 400

    # Call the cancel_reservation method
    response = reservation.cancel_reservation(reservation_id=reservation_id, idno=student.idno)

    return jsonify(response)

@main.route('/api/feedback/<record_id>', methods=['POST'])
def submit_feedback(record_id):
    global student
    try:
        # Check authorization
        if not session.get('student'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access is prohibited.'
            }), 401

        if student is None:
            student = Student(**session.get('student'))
            
        data = request.get_json()
        feedback_text = data.get('feedback')
        
        
       # Process feedback
        student.send_feedback(record_id=record_id, feedback=feedback_text)
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@main.route('/api/feedback-records')
def get_feedbacks():
    global student
    try:
        # Check authorization
        if not session.get('student'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access is prohibited.'
            }), 401

        if student is None:
            student = Student(**session.get('student'))
              
        
       # Process feedback
        feedbacks = student.retrieve_my_feedbacks(idno=student.idno)
        

        return jsonify({
            {
                'idno': feedbacks['idno'],
                
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@main.route('/api/get-lab-resources', methods=['GET'])
def get_lab_resources():
    """API to retrieve all lab resources"""
    global student
    if not session.get('student'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    if student is None:
        student = Student(**session.get('student'))

    try:
        resources = student.get_lab_resources()  

        # Convert objects to dictionaries
        resources_list = [{
            "resources_id": resource["resources_id"],
            "resources_name": resource["resources_name"],
            "description": resource["description"],
            "resource_type": resource["resource_type"],
            "resources_path": resource["resources_path"],
            "status": resource["status"],
            "upload_date": resource["upload_date"],
        } 
        for resource in resources['data']
        ]

        return jsonify({'success': True, 'resources': resources_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@main.route('/api/leaderboards')
def get_leaderboards():
    """Fetch Leaderboards"""
    global student
    if not session.get('student'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    if student is None:
        student = Student(**session.get('student'))

    try:
        leaderboards = student.retrieve_leaderboards()

        leaderboards_list = [
            {
                'Name': leaderboard['Name'],
                'Program': leaderboard['Program'],
                'session_count': leaderboard['session_count'],
                'rank': leaderboard['rank'],
                'idno': leaderboard['idno'],
                'image': leaderboard['image'],
                'points': leaderboard['points']
            }
            for leaderboard in leaderboards['data']
        ]

        total_students = len(leaderboards_list)
        current_student_id = student.idno

        current_student_entry = next((entry for entry in leaderboards_list if entry['idno'] == current_student_id), None)

        if current_student_entry:
            rank = current_student_entry['rank']
            points = current_student_entry['points']
            percentage = (1 - ((rank - 1) / total_students)) * 100
        else:
            rank = None
            percentage = None

        return jsonify({
            'success': True,
            'leaderboards': leaderboards_list,
            'student_rank': rank,
            'ranking_percentage': round(percentage, 2) if percentage is not None else None,
            'total_students': total_students,
            'points':points
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    
@main.route('/api/myRank/<idno>')
def my_rank(idno):
    """Fetch my rank"""
    global student
    try:
        # Check authentication
        if not session.get('student'):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            
        # Get rank data
        student = Student(**session.get('student'))
        rank_data = student.get_my_rank(idno=idno)
        
        if not rank_data['success']:
            return jsonify({'success': False, 'error': 'Rank not found'}), 404
            
        return jsonify({
            'success': True,
            'data': {
                'rank': rank_data['data'][0]['rank'],
                'session_count': rank_data['data'][0]['session_count'],
                'name': rank_data['data'][0]['Name'],
                'program': rank_data['data'][0]['Program']
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500




@main.route('/api/notify-reservation', methods=['POST'])
def notify_reservation():
    """Fetch reservation notifications"""
    global student
    if not session.get('student'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    if student is None:
        student = Student(**session.get('student'))

    try:
        notification = student.get_reservation_notifications(idno=student.idno)
        notification_data = notification['data'][0]
    
    except Exception as e:
        print(f"ERROR CAUGHT! 1 {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

    date_str = notification_data['reserve_date']

    try:
        reserve_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        reserve_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    now = datetime.now()

    if reserve_date.date() == now.date():
        print("Today's your reservation!")
    else:
        print("Today's not your reservation")

    return jsonify({
        'success': True,
        'data': {
            'reservation_id': notification_data['reservation_id'],
            'idno': notification_data['idno'],
            'request_date': notification_data['request_date'],
            'reserve_date': notification_data['reserve_date'],
            'lab_status': notification_data['status'],
            'message': notification_data['message'],
            'purpose': notification_data['purpose'],
            'lab_name': notification_data['lab_name'],
            'computer': notification_data['computer'],
        }
    }), 200


@main.route('/api/confirm-reservation/<reservation_id>')
def confirm_reservation(reservation_id):
    """Confirm reservation"""
    global student
    if not session.get('student'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    if student is None:
        student = Student(**session.get('student'))

    try:

        if not reservation_id:
            return jsonify({'success': False, 'error': 'Missing reservation ID or ID number'}), 400

        message = f'Hey {student.firstname}! Your reservation request is confirmed. Please be on time.'

        response = student.confirm_reservation(reservation_id=reservation_id,message=message)

        return jsonify(response), 200

    except Exception as e:
        print(f"ERROR CAUGHT! 2 {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/expire-reservation/<reservation_id>')
def expire_reservation(reservation_id):
    """Expire reservation"""
    global student
    if not session.get('student'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    if student is None:
        student = Student(**session.get('student'))

    try:

        message = f'Hey {student.firstname}! Your reservation request has expired due to not showing up in time. Please be on time next time.'

        response = student.expire_reservation(reservation_id=reservation_id,message=message)

        return jsonify(response), 200

    except Exception as e:
        print(f"ERROR CAUGHT! 3 {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
