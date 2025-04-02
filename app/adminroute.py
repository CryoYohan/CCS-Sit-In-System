from flask import make_response, session, url_for, Blueprint, render_template, request, flash, redirect, current_app, jsonify
from .modules.user_mgt_module.staff import Staff
from .modules.user_mgt_module.admin import Admin
from .modules.login_register_module import Authorization
from .database.dbhelper import Databasehelper
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import csv
import io
from reportlab.pdfgen import canvas
from docx import Document
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch


admin = Blueprint('admin', __name__, template_folder='templates/admin',url_prefix='/admin')

auth = Authorization()

admin_account = None
db = Databasehelper()

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Function to check if the file extension is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@admin.route('/login')
def adminlogin():
    return render_template('adminlogin.html')

@admin.route('/dashboard')
def dashboard():
    """Admin Dashboard"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        return render_template(
                                'admindashboard.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account
                               )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    

@admin.route('/admin_announcements')
def admin_announcements():
    """Announcements"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        response = admin_account.get_announcements_for_students()

        if response['success']:
            return render_template(
                                    'admin_announcements.html',
                                    user_in_login_page=True, 
                                    action='Logout',
                                    admin=admin_account,
                                    )
        else:
            flash('An error occured', 'error')
            return redirect(url_for('admin.dashboard'))

    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    
@admin.route('/users')
def users():
    """Users"""
    global admin_account
    dash_search = request.args.get('dash_search', None)  # Get search query from URL parameters
    
    if session.get('admin') is not None:
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        return render_template(
            'users.html',
            user_in_login_page=True,
            action='Logout',
            admin=admin_account,
            dash_search=dash_search  # Pass the search term to the template
        )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))




@admin.route('/managelab')
def managelab():
    """Manage Laboratories"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        labs = admin_account.retrieve_all_labs()

        return render_template(
                                'managelab.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account,
                                labs=labs,
                                )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    
@admin.route('/adminrecords')
def adminrecords():
    """Records"""
    global admin_account
    if not session['admin'] == None:
        
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)
        

        return render_template(
                                'adminrecords.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account,
                                )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    

@admin.route('/admin_reservation_requests')
def admin_reservation_requests():
    """Reservation Requests"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        return render_template(
                                'reservation_requests.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account,
                                )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/adminusermgt')
def adminusermgt():
    """Admin User Management"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)
            
        staffs = admin_account.retrieve_all_staff()
        

        return render_template(
                                'adminusermgt.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account,
                                staffs=staffs,
                                )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))


@admin.route('/feedbacks')
def admin_feedbacks():
    """ Admin Feedbacks Management"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        return render_template(
                                'admin_feedbacks.html',
                                user_in_login_page=True, 
                                action='Logout',
                                admin=admin_account,
                                )
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))



@admin.route('/adminlogout')
def adminlogout():
    session['admin'] = None
    flash('Admin logged out', 'error')
    return redirect(url_for('admin.adminlogin'))


@admin.route('/api/users')
def api_users():
    """API for fetching of users"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        users = admin_account.retrieve_all_students()

        # Convert objects to dictionaries
        users_list = []
        for user in users:
            users_list.append(
                {
                "idno": user['idno'],
                "firstname": user['firstname'],
                "middlename": user['middlename'],
                "lastname": user['lastname'],
                "course": user['course'],
                "year": user['year'],
                "email": user['email'],
                "session": user['session'],
                "status": user['status']
                }
            )

        return jsonify(users_list)  # Send JSON response
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    

@admin.route('/api/users/search', methods=['GET'])
def search_users():
    """API for fetching of filtered users"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        query = request.args.get('q','').strip()

        users = admin_account.retrieve_all_students()

        filtered_users = [
            {
                "idno": user['idno'],
                "firstname": user['firstname'],
                "middlename": user['middlename'],
                "lastname": user['lastname'],
                "course": user['course'],
                "year": user['year'],
                "email": user['email'],
                "session": user['session'],
                "status": user['status']
            }
            for user in users if (
                query.lower() in user['idno'].lower() or  # ✅ FIXED: user['idno'] (Dictionary)
                query.lower() in user['firstname'].lower() or
                query.lower() in user['middlename'].lower() or
                query.lower() in user['lastname'].lower() or
                query.lower() in user['email'].lower()
            )
        ]

        return jsonify(filtered_users)
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/api/users/filter-status', methods=['GET'])
def filter_status():
    """API for fetching of filtered users"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        query = request.args.get('q', '')

        users = admin_account.retrieve_all_students()

        if not query == 'all':
            filtered_users_status = [
                {
                    "idno": user['idno'],
                    "firstname": user['firstname'],
                    "middlename": user['middlename'],
                    "lastname": user['lastname'],
                    "course": user['course'],
                    "year": user['year'],
                    "email": user['email'],
                    "session": user['session'],
                    "status": user['status']
                }
                for user in users if (
                    query.lower() in user['status'].lower()  # ✅ FIXED: user['idno'] (Dictionary)
                )
            ]

            return jsonify(filtered_users_status)
        
        # Convert objects to dictionaries
        users_list = []
        for user in users:
            users_list.append(
                {
                "idno": user['idno'],
                "firstname": user['firstname'],
                "middlename": user['middlename'],
                "lastname": user['lastname'],
                "course": user['course'],
                "year": user['year'],
                "email": user['email'],
                "session": user['session'],
                "status": user['status']
                }
            )

        return jsonify(users_list)
    
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/api/users/<idno>/logoff')
def logoff(idno):
    """API to Log-off student from laboratory"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        response = admin_account.logoff_student(idno=idno, staff_idno=admin_account.idno)

        if response['success']:
            return jsonify({'success': True, 'message': 'Student logged off successfully!'})
        else:
            return jsonify({'success': False, 'message': response['message']}), 400
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/api/users/currentsitin')
def current_sitin():
    """ API for retrieving all students currently in-lab """
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        users = admin_account.retrieve_all_current_sitins()

        json_format_users = [
            {
                "idno": user['idno'],
                "firstname": user['firstname'],
                "middlename": user['middlename'],
                "lastname": user['lastname'],
                "course": user['course'],
                "year": user['year'],
                "email": user['email'],
                "session": user['session'],
                "status": user['status'],
            }
            for user in users
        ]

        return jsonify(json_format_users)
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))



@admin.route('/api/sitinrecords')
def sitinrecords():
    """API to retrieve sitin records"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        users = admin_account.retrieve_all_sitinrecords()

        # Convert objects to dictionaries
        users_list = []
        for user in users['data']:
            users_list.append({
                "record_id": user["record_id"],
                "idno": user["idno"],
                "lab_name": user["lab_name"],
                "sitin_in": user["sitin_in"],
                "sitin_out": user["sitin_out"],
                "staff_idno": user["staff_idno"],
                "logged_off_by": user["logged_off_by"],
                "status": user["status"],
                "reason": user["reason"],
            })

        return jsonify(users_list)
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    
@admin.route("/api/reservations")
def get_pending_reservations():
    """API to retrieve all reservations"""
    global admin_account

    if session.get('admin'):
        if admin_account is None:
            admin_account = session.get('admin')
            admin_account = Admin(**admin_account)

        reservations = admin_account.retrieve_all_pending_reservations()

        # Convert objects to dictionaries
        reservations_list = []
        for reservation in reservations:
            reservations_list.append({
                "reservation_id": reservation["reservation_id"],
                "idno": reservation["idno"],
                "lab_id": reservation["lab_id"],
                "reserve_date": reservation["reserve_date"],
                "request_date": reservation["request_date"],
                "status": reservation["status"]
            })

        return jsonify(reservations_list)
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
 
@admin.route('/admin_editstudent', methods=['POST'])
def admin_editstudent():
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = Admin(**session.get('admin'))

        form_data = {
            "idno": request.form["idno"],
            "firstname": request.form["firstname"],
            "middlename": request.form["middlename"],
            "lastname": request.form["lastname"],
            "email": request.form["email"],
            "course": request.form["course"],
            "year": request.form["year"],
            "password": request.form["password"],
            "confirmpassword": request.form["confirmpassword"]
        }


        if form_data['password'] != form_data['confirmpassword']:
            flash('Password do not match', 'error')
            return redirect(url_for('admin.users'))

        del form_data['confirmpassword']

        response = admin_account.update(**{k:v for k,v in form_data.items() if v != ''})


        if response['success']:
            flash(response['message'], 'success')
            return redirect(url_for('admin.users'))
        else:
            flash(response['error'], 'error')
            return redirect(url_for('admin.users'))
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/adminlogin', methods=['POST'])
def loginadmin():
    global admin_account
    idno:str = request.form['idno']
    password:str = request.form['password']

    response = auth.user_account_exist_and_correct_credentials(
                                                                idno=idno,
                                                                password=password,
                                                                url='admin',
                                                                ) 
    if response['success']:
        del response['success']
        flash('Login successful!', 'success')
        session['admin'] = response
        admin_account = Admin(**response)
        return redirect(url_for('admin.dashboard'))
    else:
        flash(response['error'], 'error')
        return redirect(url_for('admin.adminlogin'))


@admin.route('/announce', methods=['POST'])
def announce():
    """Handle Announcements Post REQUESTS"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = Admin(**session.get('admin'))

        file = request.files['image']
        filename = ''

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # Secure file name
            upload_folder = os.path.abspath(os.path.join(current_app.root_path, "static/images/announcements"))
            filepath = os.path.join(upload_folder, filename)

            if not os.path.isdir(upload_folder):
                print(f"⚠️ ERROR: Directory {upload_folder} does NOT exist!")
                flash("Upload folder missing. Contact admin.", "danger")
                return redirect(url_for('admin.admin_announcement'))
            
            print(f"Saving file to: {filepath}")  # Debugging line
            file.save(filepath.replace("\\", "/"))  # Fix Windows backslash issue

            if os.path.exists(filepath):  # Verify if the file was actually saved
                print("✅ File successfully saved!")



        announcement_data = {
            "post_title": request.form['title'],
            "post_description": request.form['description'],
            "image": filename,
            "posted_by":admin_account.idno,
            "date_posted": datetime.now(),
        }


        response = admin_account.add_announcement(**{k:v for k,v in announcement_data.items() if not v is None})
        if response['success']:
            flash('Announcement added', 'success')
            return redirect(url_for('admin.admin_announcements'))
        else:
            flash(response['error'], 'error')
            return redirect(url_for('admin.admin_announcements'))
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    

@admin.route('/api/announcements')
def get_announcements():
    """FETCH ALL ANNOUNCEMENTS"""
    global admin_account
    if not session.get('admin'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401  # Unauthorized status code

    if admin_account is None:
        admin_account = Admin(**session.get('admin'))

    response = admin_account.get_announcements_for_students()

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
    
@admin.route('/api/<post_id>/editannouncement')
def editAnnoucement(post_id):
    """Edit announcement for Admin"""
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = Admin(**session.get('admin'))

        announcement = admin_account.get_announcement(post_id=post_id)

        # In your Flask route
        if announcement['success'] and announcement['data']:
            # Assuming you only want the first announcement if multiple exist
            data = announcement['data'][0]
            return jsonify({
                'post_id': data['post_id'],
                'post_title': data['post_title'],
                'post_description': data['post_description'],
                'image': data['image'],
                'posted_by': data['posted_by'],
                'date_posted': data['date_posted'],
            })
        else:
            return jsonify({'success': False, 'message': announcement['message']}), 400
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    
@admin.route('/api/<post_id>/update', methods=['POST'])
def update_announcement_one(post_id):
    """Update an existing announcement"""
    global admin_account
    if not session.get('admin'):
        flash('Unauthorized Access', 'error')
        return redirect(url_for('admin.adminlogin'))
    
    try:
        # Initialize admin account
        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        # Get form data using same pattern as working announce() route
        update_data = {
            "post_title": request.form['editTitle'],  # Match form field name
            "post_description": request.form['editDescription'],
            "posted_by": admin_account.idno,
            "date_posted": datetime.now(),
        }

        # Handle file upload like in announce()
        if 'editPhoto' in request.files:  # Match file input name
            file = request.files['editPhoto']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = os.path.abspath(os.path.join(
                    current_app.root_path, 
                    "static/images/announcements"
                ))
                
                # Create directory if missing
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                update_data['image'] = filename

        # Update using same pattern as add_announcement
        response = admin_account.update_announcement(
            post_id=post_id,
            **{k: v for k, v in update_data.items() if v is not None}
        )
        
        if response['success']:
            return jsonify({'success': True, 'message': 'Updated'})
        else:
            return jsonify({'success': False, 'message': response['message']}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 50

    
@admin.route('/api/announcements/<post_id>', methods=['DELETE'])
def delete_announcement(post_id):
    """Delete an announcement"""
    global admin_account

    print(f"This is the announcement ID : {post_id}")

    # Check if the admin is logged in
    if not session.get('admin'):
        return jsonify({
            'success': False,
            'message': 'Unauthorized access is prohibited.'
        }), 401  # Unauthorized status code

    # Initialize admin_account if not already initialized
    if admin_account is None:
        admin_account = Admin(**session.get('admin'))

    # Delete the announcement
    response = admin_account.delete_announcement(post_id=post_id)
    print(f"Response {response}")
    # Return the response
    return jsonify(response)

@admin.route('/api/approve_reservation/<reservation_id>')
def approve_reserve(reservation_id):
    """API to approve reservation"""
    global admin_account

    if session.get('admin') is not None:
        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        response = admin_account.approve_reservation(reservation_id=reservation_id,admin=admin_account)

        if response['success']:
            return jsonify({'success': True, 'message': 'Reservation approved successfully!'})
        else:
            return jsonify({'success': False, 'message': response['message']}), 400
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/api/decline_reservation/<reservation_id>')
def decline_reserve(reservation_id):
    """API to decline reservation"""
    global admin_account

    try:
        if session.get('admin') is None:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access is prohibited'
            }), 401

        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        response = admin_account.decline_reservation(
            reservation_id=reservation_id,
            admin=admin_account
        )

        if response['success']:
            return jsonify({
                'success': True,
                'message': 'Reservation declined successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': response['message']
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@admin.route('/sitin_student', methods=['POST'])
def sitin_student():
    """Sit In Student"""
    global admin_account
    if  session.get('admin'):

        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        idno = request.form['idno']
        lab_id = request.form['lab_id']
        reason = request.form['reason']

        if lab_id == "#" or reason == "#":
            return jsonify({'success': False, 'error': 'Please select a valid lab and purpose'}), 400

        response = admin_account.sit_in_student(idno=idno, lab_id=lab_id, reason=reason, staff_idno=admin_account.idno)

        if response['success']:
            return jsonify({'success': True, 'message': 'Student successfully sat in'})

        return jsonify({'success': False, 'error': response['error']}), 400
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))



@admin.route('/addstaff', methods=['POST'])
def addstaff():
    global admin_account
    if not session['admin'] == None:
        if admin_account == None:
            admin_account = Admin(**session.get('admin'))

        
        staff_data = {
                    'idno': request.form.get('idno'),
                    'firstname': request.form.get('firstname'),
                    'middlename': request.form.get('middlename'),
                    'lastname': request.form.get('lastname'),
                    'email': request.form.get('email'),
                    'course': request.form.get('course', ''),  # Default to empty string if not provided
                    'year': request.form.get('year', ''),  
                    'image': None,    # Set to None but will have new value later
                    }   

        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        if password != confirmpassword:
            flash('Password do not match', 'error')
            return redirect(url_for('admin.adminusermgt'))
        
        


        staff = Staff(**{k: v for k, v in staff_data.items() if v != ''})
        print(staff.__dict__)

        response = admin_account.add_staff(**staff.__dict__,password=password)

        if response['success']:
            flash('Successfully added','success')
            return redirect(url_for('admin.adminusermgt'))
        else:
             flash(response['error'],'error')
             return redirect(url_for('admin.adminusermgt'))
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))
    

@admin.route('/api/feedbacks')
def fetch_feedbacks():
    """ API for fetching feedbacks"""
    global admin_account

    if session.get('admin') is not None:
        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        feedbacks = admin_account.retrieve_all_feedbacks()

        json_formatted_data = [
            {
                "feedback_id": feedback['feedback_id'],
                "idno": feedback['idno'],
                "lab_name": feedback['lab_name'],
                "feedback": feedback['feedback'],
                "submitted_on": feedback['submitted_on'],
                "reason": feedback['reason']
            }
            for feedback in feedbacks['data']
        ]

        return jsonify(
            json_formatted_data
        )

    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/api/feedback/<feedback_id>')
def get_feedback(feedback_id):
    """ API for fetching single feedback by ID """
    global admin_account

    if session.get('admin') is not None:
        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        feedbacks = admin_account.retrieve_one_feedback(feedback_id=feedback_id)

        # Debug print to check the structure
        print(f"Raw feedback data: {feedbacks}")
        
        if not feedbacks.get('data') or not feedbacks['data']:
            return jsonify({"error": "Feedback not found"}), 404

        # Get the first feedback directly
        feedback = feedbacks['data'][0]
        print(f"Lab name: {feedback['lab_name']}")  # Debug print

        # Create response object directly
        response_data = {
            "feedback_id": feedback['feedback_id'],
            "idno": feedback['idno'],
            "lastname": feedback['lastname'],
            "firstname": feedback['firstname'],
            "lab_name": feedback['lab_name'],
            "feedback": feedback['feedback'],
            "submitted_on": feedback['submitted_on'],
            "reason": feedback['reason']
        }

        return jsonify(response_data)

    else:
        return jsonify({"error": "Unauthorized"}), 401


@admin.route('/api/records-by-lab/<lab_name>')
def fetch_records_by_lab(lab_name):
    """Fetch records by lab"""
    global admin_account

    if session.get('admin') is not None:
        if admin_account is None:
            admin_account = Admin(**session.get('admin'))

        records = admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)


        json_formatted_data = [
            {
                "record_id": record['record_id'],
                "idno": record['idno'],
                "lab_name": record['lab_name'],
                "sitin_in": record['sitin_in'],
                "sitin_out": record['sitin_out'],
                "staff_idno": record['staff_idno'],
                "logged_off_by": record['logged_off_by'],
                "status": record['status'],
                "reason": record['reason']
            }
            for record in records['data']
        ]
        return jsonify(json_formatted_data)

    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))


@admin.route('/api/export-records/csv/<lab_name>')
@admin.route('/api/export-records/csv')
def export_records_csv(lab_name=None):
    """Export records to CSV"""
    global admin_account
    if session.get('admin') is None:
        return redirect(url_for('admin.adminlogin'))

    if admin_account is None:
        admin_account = Admin(**session.get('admin'))

    # Get filtered records
    records = admin_account.retrieve_sitinrecord_by_lab(lab_id=lab_name) if lab_name else admin_account.retrieve_all_sitinrecords()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Record ID', 'Student ID', 'Lab', 'Check-in', 'Check-out', 
                    'Staff ID', 'Logged Off By', 'Status', 'Reason'])
    
    # Write data
    for record in records:
        writer.writerow([
            record['record_id'],
            record['idno'],
            record['lab_name'],
            record['sitin_in'],
            record['sitin_out'] or '',
            record['staff_idno'] or '',
            record['logged_off_by'] or '',
            record['status'],
            record['reason'] or ''
        ])
    
    # Prepare response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=sit_in_records.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@admin.route('/api/export-records/excel/<lab_name>/<purpose>')
def export_records_excel(lab_name=None,purpose=None):
    """Export records to Excel"""
    global admin_account
    if session.get('admin') is None:
        return redirect(url_for('admin.adminlogin'))

    if admin_account is None:
        admin_account = Admin(**session.get('admin'))

    if lab_name and lab_name != 'all' and purpose and purpose != 'all':
    # Filter by both lab_name and purpose
        print("IF CONDITION")
        records = admin_account.retrieve_sitinrecord_by_lab_and_purpose(lab_name=lab_name, reason=purpose)
    elif lab_name and lab_name != 'all':
        print("1st elif CONDITION")
        # Filter by lab_name only
        records = admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
    elif purpose and purpose != 'all':
        print("2ND elif CONDITION")
        # Filter by purpose only
        records = admin_account.retrieve_sitinrecord_by_purpose(reason=purpose)
        print(records)
    else:
        # No filters applied, retrieve all records
        print("ELSE CONDITION")
        records = admin_account.retrieve_all_sitinrecords()
#    # Fetch records
#     records = (admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
#                if lab_name and lab_name != 'all' else admin_account.retrieve_all_sitinrecords())

    # Create DataFrame
    df = pd.DataFrame([{
        'Record ID': r['record_id'],
        'Student ID': r['idno'],
        'Lab': r['lab_name'],
        'Check-in': r['sitin_in'],
        'Check-out': r['sitin_out'] or '',
        'Staff ID': r['staff_idno'] or '',
        'Logged Off By': r['logged_off_by'] or '',
        'Status': r['status'],
        'Reason': r['reason'] or ''
    } for r in records['data']])  # Assuming all keys exist


    # Create Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sit-In Records')
        writer.close()  # Correct method

    output.seek(0)

    # Prepare response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=sit_in_records_lab-{lab_name}_purpose-{purpose}.xlsx'
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return response

@admin.route('/api/export-records/pdf/<lab_name>/<purpose>')
def export_records_pdf(lab_name=None, purpose=None):
    """Generate a well-formatted PDF for Sit-In Records."""
    global admin_account
    if session.get('admin') is None:
        return redirect(url_for('admin.adminlogin'))

    if admin_account is None:
        admin_account = Admin(**session.get('admin'))
    
    if lab_name and lab_name != 'all' and purpose and purpose != 'all':
    # Filter by both lab_name and purpose
        print("IF CONDITION")
        records = admin_account.retrieve_sitinrecord_by_lab_and_purpose(lab_name=lab_name, reason=purpose)
    elif lab_name and lab_name != 'all':
        print("1st elif CONDITION")
        # Filter by lab_name only
        records = admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
    elif purpose and purpose != 'all':
        print("2ND elif CONDITION")
        # Filter by purpose only
        records = admin_account.retrieve_sitinrecord_by_purpose(reason=purpose)
        print(records)
    else:
        # No filters applied, retrieve all records
        print("ELSE CONDITION")
        records = admin_account.retrieve_all_sitinrecords()

    
    # # Fetch records
    # records = (
    #     admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
    #            if lab_name and lab_name != 'all' else admin_account.retrieve_all_sitinrecords())
    
    filename = f"sit_in_records_lab_{lab_name}.pdf" if lab_name else "sit_in_records_all.pdf"
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(letter), leftMargin=30, rightMargin=30, topMargin=50, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph(f"Sit-In Records - {lab_name if lab_name else 'All Labs'}", styles['Title'])
    elements.append(title)
    
    # Table Headers
    data = [['Record ID', 'Student ID', 'Lab', 'Check-in', 'Check-out', 'Status', 'Reason']]
    
    # Add Data Rows
    for record in records['data']:
        data.append([
            str(record['record_id']),
            str(record['idno']),
            record['lab_name'],
            format_date(record['sitin_in']),
            format_date(record['sitin_out']),
            record['status'],
            record['reason'] or ''
        ])
    
    # Create Table
    table = Table(data, colWidths=[70, 80, 60, 120, 120, 70, 140])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10)
    ]))
    
    elements.append(table)
    doc.build(elements)
    output.seek(0)

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'application/pdf'
    return response

def format_date(datetime_str):
    """Format datetime string for display, handling milliseconds"""
    if not datetime_str:
        return ''
    
    try:
        # Try parsing with milliseconds first
        try:
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            # Fall back to parsing without milliseconds
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%m/%d/%Y %I:%M %p')
    except ValueError as e:
        print(f"Error formatting date: {datetime_str} - {str(e)}")
        return datetime_str  # Return original string if formatting fails

@admin.route('/api/export-records/word/<lab_name>/<purpose>')
def export_records_word(lab_name=None, purpose=None):
    """Export records to Word"""
    global admin_account
    if session.get('admin') is None:
        return redirect(url_for('admin.adminlogin'))

    if admin_account is None:
        admin_account = Admin(**session.get('admin'))
    
    if lab_name and lab_name != 'all' and purpose and purpose != 'all':
    # Filter by both lab_name and purpose
        print("IF CONDITION")
        records = admin_account.retrieve_sitinrecord_by_lab_and_purpose(lab_name=lab_name, reason=purpose)
    elif lab_name and lab_name != 'all':
        print("1st elif CONDITION")
        # Filter by lab_name only
        records = admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
    elif purpose and purpose != 'all':
        print("2ND elif CONDITION")
        # Filter by purpose only
        records = admin_account.retrieve_sitinrecord_by_purpose(reason=purpose)
        print(records)
    else:
        # No filters applied, retrieve all records
        print("ELSE CONDITION")
        records = admin_account.retrieve_all_sitinrecords()

    # # Fetch records
    # records = (admin_account.retrieve_sitinrecord_by_lab(lab_name=lab_name)
    #            if lab_name and lab_name != 'all' else admin_account.retrieve_all_sitinrecords())

    # Create Word document
    document = Document()
    document.add_heading('Sit-In Records', 0)
    
    # Create table
    table = document.add_table(rows=1, cols=7)
    table.style = 'Table Grid'
    
    # Add headers
    headers = table.rows[0].cells
    headers[0].text = 'Record ID'
    headers[1].text = 'Student ID'
    headers[2].text = 'Lab'
    headers[3].text = 'Check-in'
    headers[4].text = 'Check-out'
    headers[5].text = 'Status'
    headers[6].text = 'Reason'
    
    # Add data
    for record in records['data']:
        row = table.add_row().cells
        row[0].text = str(record['record_id'])
        row[1].text = str(record['idno'])
        row[2].text = record['lab_name']
        row[3].text = record['sitin_in']
        row[4].text = record['sitin_out'] or ''
        row[5].text = record['status']
        row[6].text = record['reason'] or ''
    
    # Save to memory
    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    # Prepare response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=sit_in_records_lab-{lab_name}_purpose-{purpose}.docx'
    response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    return response



