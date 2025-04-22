from ..database.dbhelper import Databasehelper
from .security.hashpw import PasswordHashing
from random import choice
# from .user_mgt_module.student import Student
# from .user_mgt_module.admin import Admin
# from .user_mgt_module.staff import Staff
class Authorization():
    def __init__(self):
        self.profileicons = ['bear.png','cat.png','chicken.png', 'meerkat.png','panda.png','polar-bear.png', 'shark.png','weasel.png','wolf.png']
        self.db = Databasehelper()
        self.hashpasword = PasswordHashing()

    def user_account_exist_and_correct_credentials(self, idno: str, password: str,url:str)->dict:
        """Check if a student account exists and return a Student instance if valid."""
        try:
            student_exists = self.db.find_record('user', idno=idno)

            if student_exists:
                for data in student_exists:
                    try:
                        if data['role'] == 'Student' and url == 'student':
                            password_correct = self.hashpasword.check_password(password, data['password'])
                            if password_correct:
                                return {
                                        'success': True,
                                        'idno': data['idno'],
                                        'firstname': data['firstname'],
                                        'middlename': data['middlename'],
                                        'lastname': data['lastname'],
                                        'course': data['course'],
                                        'year': data['year'],
                                        'email': data['email'],
                                        'image': data['image'],
                                        'session': data['session'],
                                        }
                            else:
                                return {'success': False, 'error' :'Password incorrect!' }
                                   

                        elif data['role'] == 'Admin' and url == 'admin':
                            password_correct = self.hashpasword.check_password(password, data['password'])

                            if password_correct:
                                return {
                                    'success': True,
                                    'idno': data['idno'],
                                    'firstname': data['firstname'],
                                    'middlename': data['middlename'],
                                    'lastname': data['lastname'],
                                    'email': data['email'],
                                    'image': data['image']
                                }

                            else:
                                return {'success':False, 'error': 'Password incorrect!' }
                            
                        elif data['role'] == 'Staff' and url == 'staff':
                            password_correct = self.hashpasword.check_password(password, data['password'])
                    
                            if password_correct:
                                return {
                                    'success': True,
                                    'idno': data['idno'],
                                    'firstname': data['firstname'],
                                    'middlename': data['middlename'],
                                    'lastname': data['lastname'],
                                    'email': data['email'],
                                    'course': data['course'],
                                    'year': data['year'],
                                    'image': data['image'],
                                }
                            else:
                                return {'success': False, 'error': 'Password incorrect!'}

                        else:
                            return {'success': False, 'error': 'Unknown User Credentials'}


                    except Exception as e:
                        return {'success': False, 'error': str(e)}           
            else:
                return {'success': False, 'error' :'User does not exist.'}

        except Exception as e:
            return {'success': False, 'error': str(e)}
                
    def user_is_registered(self, **kwargs
                           ) ->dict:
        """Register a user and return a Student instance if successful."""

        users = self.db.getall_records('user')

        user_exist = [user['idno'] for user in users if user['idno'] == kwargs.get('idno')]
        email_exist =  [user['email'] for user in users if user['email'] == kwargs.get('email')]
        # Check if email input already exists in database
        if kwargs.get('email') in email_exist:
            print(f"EMAIL EXISTS{kwargs.get('email')}\EMAIL EXISTING{email_exist}")
            return {'success': False,'error' : 'Email already in use. Please try a different email'}
        
        if kwargs.get('idno') in user_exist:
             return {'success': False,'error' : 'User already exists!'}

        if kwargs.get('url')=='student':
            try:
                hashed_password = self.hashpasword.hashpassword(kwargs.get('password'))

                student_add_data_to_object = {k:v for k,v in kwargs.items() if not k == 'password' and not k == 'url'}
                student_add_data_to_object['image'] = None
                student_add_data_to_object['session'] = 30 # Add default amount of session
                
                # session['student'] = student.__dict__ 

                student_add_data_to_object['password'] = hashed_password
                student_add_data_to_object['image'] = choice(self.profileicons) # Add random profile icon
                student_add_data_to_object['session'] = 30 # Add default amount of sessions
                student_add_data_to_object['points'] = 0 # Add default points

                self.db.add_record(table='user',**student_add_data_to_object) 

                del student_add_data_to_object['password']
                student_add_data_to_object['success'] = True

                return student_add_data_to_object  

            except Exception as e:
                return {'success': False, 'error': str(e)}

        else:
            return {'success': False, 'error':'User already exists'}
            
            

