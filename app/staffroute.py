from flask import Flask, url_for, redirect, Blueprint, session, render_template, request, flash
from .modules.login_register_module import Authorization
from .modules.user_mgt_module.staff import Staff
from .modules.reservation_module.reserve_lab import Reservation

staff = Blueprint("staff", __name__,template_folder='templates/staff',url_prefix='/staff')

auth = Authorization()

staff_account = None

reservation = Reservation()

@staff.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@staff.route('/dashboard')
def dashboard():
    """Staff Dashboard"""
    global staff_account
    if session['staff'] == None:
        return redirect(url_for('staff.login'))
    
    if staff_account == None:
        staff_data = session.get('staff')
        staff_account = Staff(**staff_data)
    
    if session.get('lab') == None:
        flash('No lab assigned. Please select a lab.', 'error')
        return redirect(url_for('staff.staff_select_lab'))
        
    lab_name = session.get('lab')

    return render_template('staffdashboard.html',user_in_login_page=True, action='Logout',staff=staff_account,lab_name=lab_name)

       
    
@staff.route('/managerequest')
def managerequest():
    """Staff Sit-in Management"""
    global staff_account
    if session['staff'] == None:
        return redirect(url_for('staff.login'))
    
    if staff_account == None:
        staff_data = session.get('staff')
        staff_account = Staff(**staff_data)
    
    if session.get('lab') == None:
        flash('No lab assigned. Please select a lab.', 'error')
        return redirect(url_for('staff.staff_select_lab'))
        
    records = reservation.retrieve_sitinrecords(idno=None)

    return render_template('managerequest.html',user_in_login_page=True, action='Logout',staff=staff_account, records=records)
    
    
@staff.route('/staffusermgt')
def staffusermgt():
    """Staff User Management"""
    global staff_account
    if session['staff'] == None:
        return redirect(url_for('staff.login'))
    
    if staff_account == None:
        staff_data = session.get('staff')
        staff_account = Staff(**staff_data)
    
    if session.get('lab') == None:
        flash('No lab assigned. Please select a lab.', 'error')
        return redirect(url_for('staff.staff_select_lab'))
        

    return render_template('staffusermgt.html',user_in_login_page=True, action='Logout',staff=staff_account)


@staff.route('/login')
def login():
    return render_template('stafflogin.html')

@staff.route('/staff_select_lab')
def staff_select_lab():
    """Staff Lab Selection"""
    global staff_account
    if not session['staff'] == None:

        if staff_account == None:
            staff_data = session.get('staff')
            staff_account = Staff(**staff_data)

    return render_template('staff_lab_selection.html',user_in_login_page=True, action='Logout',staff=staff_account)

@staff.route('/logout')
def logout():
    """Staff Logout"""
    global staff_account
    session['staff'] = None
    staff_account = None
    session['lab'] = None
    message = "Staff have been logged out."
    flash(message, 'success')
    return redirect(url_for('staff.login'))

@staff.route('/loginstaff', methods=['POST'])
def loginstaff():
    global staff_account
    idno = request.form['idno']
    password = request.form['password']

    response = auth.user_account_exist_and_correct_credentials(idno=idno, password=password, url='staff')
    if response['success']:
        del response['success']
        flash('Login successful!', 'success')
        session['staff'] = response
        staff_account = Staff(**response)

        # Render a template with a modal for lab selection
        return render_template('staff_lab_selection.html', staff=staff_account)
    else:
        flash(response['error'], 'error')
        return redirect(url_for('staff.login'))

@staff.route('/select_lab', methods=['POST'])
def select_lab():
    lab_name = request.form['lab_name']
    session['lab'] = lab_name  # Store the selected lab in the session
    flash(f'Lab "{lab_name}" has been assigned.', 'success')
    return redirect(url_for('staff.dashboard'))