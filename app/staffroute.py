from flask import Flask, url_for, redirect, Blueprint, session, render_template,request,flash
from .modules.login_register_module import Authorization

auth = Authorization()
staff = Blueprint("staff", __name__,template_folder='templates/staff', url_prefix='/staff')


@staff.route('/login')
def login():
    return render_template('stafflogin.html')

@staff.route('/adminlogin', methods=['POST'])
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
