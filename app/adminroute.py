from flask import session, url_for, Blueprint, render_template, request, flash, redirect, current_app, jsonify
from .modules.user_mgt_module.staff import Staff
from .modules.user_mgt_module.admin import Admin
from .modules.login_register_module import Authorization
from .database.dbhelper import Databasehelper
from werkzeug.utils import secure_filename
import os
from datetime import datetime

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
        for user in users:
            users_list.append({
                "record_id": user["record_id"],
                "reservation_id": user["reservation_id"],
                "idno": user["idno"],
                "lab_id": user["lab_id"],
                "sitin_in": user["sitin_in"],
                "sitin_out": user["sitin_out"],
                "staff_idno": user["staff_idno"],
                "logged_off_by": user["logged_off_by"],
                "status": user["status"],
                "reason": user["reason"],
                "completed_at": user["completed_at"]
            })

        return jsonify(users_list)
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

        post_title = request.form['editTitle']
        post_description = request.form['editDescription']
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

    
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


        staff = Staff(**{k: v for k, v in staff_data.items()})
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







