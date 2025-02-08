from flask import session, url_for, Blueprint, render_template
from .modules.user_mgt_module.staff import Staff
from .modules.user_mgt_module.admin import Admin
from .modules.login_register_module import Authorization

admin = Blueprint('admin', __name__)

auth = Authorization()


@admin.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

