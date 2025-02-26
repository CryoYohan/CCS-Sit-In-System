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
    if not session['staff'] == None:
         
        if staff_account == None:
            staff_data = session.get('staff')
            staff_account = Staff(**staff_data)

        return render_template('staffdashboard.html',user_in_login_page=True, action='Logout',staff=staff_account)

    else:
        return redirect(url_for('staff.login'))
    
@staff.route('/managesitin')
def managesitin():
    """Staff Sit-in Management"""
    global staff_account
    if not session['staff'] == None:

        if staff_account == None:
            staff_data = session.get('staff')
            staff_account = Staff(**staff_data)
        
        records = reservation.retrieve_sitinrecords(idno=None)

        return render_template('managesitin.html',user_in_login_page=True, action='Logout',staff=staff_account, records=records)

    else:
        return redirect(url_for('staff.login'))
    
    
@staff.route('/staffusermgt')
def staffusermgt():
    """Staff User Management"""
    global staff_account
    if not session['staff'] == None:

        if staff_account == None:
            staff_data = session.get('staff')
            staff_account = Staff(**staff_data)

        return render_template('staffusermgt.html',user_in_login_page=True, action='Logout',staff=staff_account)

    else:
        return redirect(url_for('staff.login'))


@staff.route('/login')
def login():
    return render_template('stafflogin.html')

@staff.route('/logout')
def logout():
    session['staff'] = None
    message = "Staff have been logged out."
    flash(message, 'success')
    return redirect(url_for('staff.login'))

@staff.route('/loginstaff', methods=['POST'])
def loginstaff():
    global staff_account
    idno:str = request.form['idno']
    password:str = request.form['password']

    response = auth.user_account_exist_and_correct_credentials(idno=idno,password=password,url='staff') 
    if response['success']:
        del response['success']
        flash('Login successful!', 'success')
        session['staff'] = response
        staff_account = Staff(**response)
        return redirect(url_for('staff.dashboard'))
    else:
        flash(response['error'], 'error')
        return redirect(url_for('staff.login'))