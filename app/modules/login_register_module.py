from ..database.dbhelper import Databasehelper
from ..modules.hashpw import PasswordHashing
from flask import session


class Authorization():
    def __init__(self):
        self.db = Databasehelper()
        self.hashpasword = PasswordHashing()

    def student_account_exist_and_correct_credentials(self,idno:str, password:str)->bool:
        """Check if a student account exists."""
        student_exists = self.db.find_record('student',idno)
        if student_exists:
            for data in student_exists:
                try:
                    password_correct = self.hashpasword.check_password(password, data['password'])
                    if password_correct:
                        session['student'] = {
                        'idno': data['idno'],
                        'fullname': data['fullname'],
                        'course': data['course'],
                        'year': data['year']
                        }
                        return True
                    else:
                        return False
                except Exception as e:
                    print(e)
                    return False            
        else:
            return False
    
    def student_is_registered(self,idno:str,fullname:str,course:str,year:int,email:str,password:str)->None:
        """Register a student record."""
        try:
            hashed_password = self.hashpasword.hashpassword(password)

            self.db.add_record('student',idno=idno,fullname=fullname,course=course,year=year,email=email,password=hashed_password)

            session['student'] = {
                'idno': idno,
                'fullname': fullname,
                'course': course,
                'year': year
            }

            return True
        except Exception as e:
            print(e)    
            return False
