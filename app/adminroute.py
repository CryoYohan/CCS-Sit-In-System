from flask import session, url_for, Blueprint, render_template, request, flash, redirect
from .modules.user_mgt_module.staff import Staff
from .modules.user_mgt_module.admin import Admin
from .modules.login_register_module import Authorization
from .database.dbhelper import Databasehelper

admin = Blueprint('admin', __name__, template_folder='templates/admin',url_prefix='/admin')

auth = Authorization()

admin_account = None
db = Databasehelper()

@admin.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@admin.route('/login')
def adminlogin():
    return render_template('adminlogin.html')

@admin.route('/dashboard')
def dashboard():
    if not session['admin'] == None:
        return render_template('admindashboard.html')
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/adminusermgt')
def adminusermgt():
    if not session['admin'] == None:
        return render_template('adminusermgt.html',user_in_login_page=True, action='Logout',admin=True)
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))

@admin.route('/adminlogout')
def adminlogout():
    session['admin'] = None
    flash('Admin logged out', 'error')
    return redirect(url_for('admin.adminlogin'))

@admin.route('/adminlogin', methods=['POST'])
def loginadmin():
    idno:str = request.form['idno']
    password:str = request.form['password']

    legit_admin = auth.user_account_exist_and_correct_credentials(idno=idno,password=password) 
    if legit_admin:
        flash('Login successful!', 'success')
        session['admin'] = legit_admin.__dict__
        return redirect(url_for('admin.adminusermgt'))
    else:
        return redirect(url_for('admin.adminlogin'))


@admin.route('/addstaff', methods=['POST'])
def addstaff():
    global admin_account
    if not session['admin'] == None:
        staff_data = request.form.to_dict()
        hashed_password = ""

        password = staff_data.pop('password',None)
        confirmpassword = staff_data.pop('confirm_password',None)

        if password and password != confirmpassword:
            print(password, confirmpassword)
            flash('Passwords do not match!', 'error')
            return redirect(url_for('admin.adminusermgt'))

        add_data = {
            "idno": staff_data.get("idno"),
            "firstname": staff_data.get("firstname"),
            "middlename": staff_data.get("middlename"),
            "lastname": staff_data.get("lastname"),
            "course": staff_data.get("course"),
            "year":staff_data.get("year"),
            "email": staff_data.get("email"),
        }
        staff_account = Staff(**add_data)
        # Hash password
        add_data = admin_account.__dict__.copy()
        if password:
            hashed_password = auth.hashpasword.hashpassword(password)
            add_data['password'] = hashed_password
        
        try:
            if add_data:
                print(f"ADD DATA DICT =>{add_data}")
                db.add_record(table='user',**{k:v for k,v in add_data.items() if v})
                del add_data['password']

                flash('Successfully added','success')
                return redirect(url_for('admin.adminusermgt'))
            else:
                flash('No Changes made')
                return redirect(url_for('admin.adminusermgt'))

        except Exception as e:
            flash(str(e),'error')
    else:
        flash('Unauthorized Access is Prohibited', 'error')
        return redirect(url_for('admin.adminlogin'))








