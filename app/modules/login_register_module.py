from ..database.dbhelper import Databasehelper
from .security.hashpw import PasswordHashing
from flask import session, flash


class Authorization():
    def __init__(self):
        self.db = Databasehelper()
        self.hashpasword = PasswordHashing()

    def user_account_exist_and_correct_credentials(self,idno:str, password:str)->bool:
        """Check if a student account exists."""
        student_exists = self.db.find_record('user',idno)
        if student_exists:
            for data in student_exists:
                try:
                    password_correct = self.hashpasword.check_password(password, data['password'])
                    if password_correct:
                        session['student'] = {
                        'idno': data['idno'],
                        'firstname': data['firstname'],
                        'middlename': data['middlename'],
                        'lastname': data['lastname'],
                        'course': data['course'],
                        'year': data['year'],
                        'email': data['email'],
                        }
                        return True
                    else:
                        print("Password is incorrect.")
                        return False
                except Exception as e:
                    print(e)
                    return False            
        else:
            print("User does not exist.")
            return False
    
    def user_is_registered(self,idno:str,firstname:str,middlename:str,lastname:str,course:str, year:int,email:str,password:str)->None:
        """Register a student record."""
        student_exist = self.db.find_record('user',idno)
        if not student_exist:
            try:
                hashed_password = self.hashpasword.hashpassword(password)

                self.db.add_record('user',idno=idno,firstname=firstname,middlename=middlename,lastname=lastname,course=course,year=year,email=email,password=hashed_password)

                session['student'] = {
                    'idno': idno,
                    'firstname': firstname,
                    'middlename': middlename,
                    'lastname': lastname,
                    'course': course,
                    'year': year,
                    'email': email,
                }

                return True
            except Exception as e:
                print(e)    
                return False
        else:
            flash("User already exists.",'error')
            return False
