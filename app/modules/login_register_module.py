from ..database.dbhelper import Databasehelper
from .security.hashpw import PasswordHashing
from .user_mgt_module.student import Student
from .user_mgt_module.admin import Admin
from .user_mgt_module.staff import Staff
from flask import session, flash
import sqlite3


class Authorization():
    def __init__(self):
        self.db = Databasehelper()
        self.hashpasword = PasswordHashing()

    def user_account_exist_and_correct_credentials(self, idno: str, password: str,url:str) -> Student | Admin | Staff | None:
        """Check if a student account exists and return a Student instance if valid."""
        try:
            student_exists = self.db.find_record('user', idno=idno)

            if student_exists:
                for data in student_exists:
                    try:
                        if data['role'] == 'Student' and url == 'student':
                            password_correct = self.hashpasword.check_password(password, data['password'])
                            if password_correct:
                                student = Student(
                                                idno=data['idno'],
                                                firstname=data['firstname'],
                                                middlename=data['middlename'],
                                                lastname=data['lastname'],
                                                course=data['course'],
                                                year=data['year'],
                                                email=data['email'],
                                                image = data['image'],
                                                session = data['session'],
                                            )
                                # session['student'] = student.__dict__  # Store Student object as a dictionary in session
                                return student
                            else:
                                flash("Password is incorrect.",'error')
                                return None
                        elif data['role'] == 'Admin' and url == 'admin':
                            password_correct = self.hashpasword.check_password(password, data['password'])

                            if password_correct:
                                admin = Admin(
                                            idno=data['idno'],
                                            firstname=data['firstname'],
                                            middlename=data['middlename'],
                                            lastname=data['lastname'],
                                            email=data['email'],
                                            image = data['image'],
                                        )
                                # session['student'] = student.__dict__  # Store Student object as a dictionary in session
                                return admin
                            else:
                                flash("Password is incorrect.",'error')
                                return None
                        elif data['role'] == 'Staff' and url == 'staff':
                            password_correct = self.hashpasword.check_password(password, data['password'])
                            print(f"STAFF PASS {password_correct} PASS INPUT {password}")
                            if password_correct:
                                staff = Staff(
                                            idno=data['idno'],
                                            firstname=data['firstname'],
                                            middlename=data['middlename'],
                                            lastname=data['lastname'],
                                            email=data['email'],
                                            course=data['course'],
                                            year=data['year'],
                                            image = data['image'],
                                        )
                                # session['student'] = student.__dict__  # Store Student object as a dictionary in session
                                return staff
                            else:
                                flash("Password is incorrect. Staff",'error')
                                return None
                        else:
                            flash("Unknown user credentials.",'error')
                            return None

                    except Exception as e:
                        flash(e)
                        return None            
            else:
                flash("User does not exist.",'error')
                return None
        except Exception as e:
            flash(str(e), 'error')
            return None
    
    def user_is_registered(self, **kwargs
                           ) -> Student | Staff | None:
        
        """Register a user and return a Student instance if successful."""
        users = self.db.getall_records('user')
        user_exist = [user['idno'] for user in users if user['idno'] == kwargs.get('idno')]
        email_exist =  [user['email'] for user in users if user['email'] == kwargs.get('email')]

        if not user_exist and kwargs.get('url')=='student':
            try:
                 # Check if email input already exists in database
                if kwargs.get('email') == email_exist:
                    flash('Email already in use. Please try a different email', 'error')
                    return None
                
                else:
                    hashed_password = self.hashpasword.hashpassword(kwargs.get('password'))

                    student_add_data_to_object = {k:v for k,v in kwargs.items() if not k == 'password' and not k == 'url'}
                    student_add_data_to_object['image'] = None
                    student_add_data_to_object['session'] = 30 # Add default amount of session

                    student = Student(**student_add_data_to_object)
                    
                    # session['student'] = student.__dict__ 

                    student_data = student.__dict__.copy()
                    student_data['password'] = hashed_password
                    student_data['image'] = student.random_profile() # Add random profile icon
                    self.db.add_record(table='user',**student_data) 

                    del student_data['password']

                    return student    

            except Exception as e:
                flash(str(e),'error')
                return None
            
        else:
            try:
                # Check if email input already exists in database
                if kwargs.get('email') == email_exist:
                    flash('Email already in use. Please try a different email', 'error')
                    return None
                
                else:
                    staff_add_data_to_object = {k:v for k,v in kwargs.items() if not k == 'password' and not k == 'url'}
                    staff_add_data_to_object['image'] = None

                    staff = Staff(**staff_add_data_to_object)
                    
                    # session['student'] = student.__dict__ 

                    staff_data = staff.__dict__.copy()
                    staff_data['password'] = kwargs.get('password')
                    staff_data['image'] = staff.random_profile() # Add random profile icon
                    self.db.add_record(table='user',**staff_data) 
                    
                    del staff_data['password']

                    return staff
                
            except Exception as e:
                flash(str(e),'error')
                return None
            
            

