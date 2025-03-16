from .user import User
from ..security.hashpw import PasswordHashing
from random import choice
from datetime import datetime

class Admin(User):
    auth = PasswordHashing()
    def __init__(self,idno:str, firstname:str, middlename:str, lastname:str, email:str,image:str, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role
        self.image = image

    def add_staff(self,**kwargs):
        """Add a new Staff"""
        password = kwargs.get("password")
        kwargs['password'] = self.auth.hashpassword(password)
        kwargs['image'] = choice(self.profileicons)

        print(f'Data to insert to table{kwargs}')
        
        try:
            self.db.add_record(table='user',**kwargs) 
            del kwargs['password']
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def retrieve_all_staff(self):
        """Retrieve all staff"""
        return self.db.getall_records_rolebased(role='Staff')

    def retrieve_all_students(self):
        """Retrieve all students"""
        return self.db.getall_records_rolebased(role='Student')

    def retrieve_all_students_to_sitin(self):
        """ Retrieve all students joined sitin reservation"""
        return self.db.retrieve_all_students_to_sitin()
    
    def retrieve_all_users(self):
        """Retrieve all users"""
        return self.db.get_all_users()

    def retrieve_all_labs(self):
         """Retrieve all labs"""
         return self.db.getall_records(table='lab')

    def retrieve_all_current_sitins(self):
        """ Retrieve all students who currently in lab"""
        return self.db.retrieve_all_current_sitins()



    def add_announcement(self, **kwargs):
        """Add an announcement"""
        try:
            self.db.add_record(table='announcement',**kwargs) 
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}

    
    def retrieve_all_sitinrecords(self):
        """Retrieve all Joined Sitin Records"""
        try:
            sitinrecords = self.db.getall_sitinrecords(idno=None)
            return{'success':True, 'sitinrecords':sitinrecords}
        
        except Exception as e:
            return {'erorr':str(e)}
    
    def sit_in_student(self,**kwargs):
        """Sit in a student"""
        sitin_datetime = datetime.now()
        kwargs['sitin_in'] = sitin_datetime
        kwargs['status'] = 'In-lab'
        try:
            self.db.add_record(table='sitin_reservation',**kwargs)
            return {'success':True}
        except Exception as e:
            return {'success':False, 'error':str(e)}

    def logoff_student(self, idno,staff_idno):
        """Log-off student"""
        try:
            reservation = self.db.find_record(table='sitin_reservation',idno=idno)
            self.db.update_record(table='sitin_reservation', idno=idno, status='Idle')

            data={
                    'reservation_id': reservation[0]['reservation_id'],
                    'idno': reservation[0]['idno'],
                    'lab_id': reservation[0]['lab_id'],
                    'sitin_in': reservation[0]['sitin_in'],
                    'sitin_out': datetime.now(),  # Log the current time
                    'staff_idno': reservation[0]['staff_idno'],
                    'logged_off_by': staff_idno,  # Admin/Staff who logs off the student
                    'status': 'Completed',
                    'reason': reservation[0]['reason'],
                    'completed_at': datetime.now()
            }
            
            # Insert into sitin_record with the correct log-off time and logged_off_by
            self.db.add_record(
                table='sitin_record',
                **data
            )
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}



    def update(self, **kwargs):
        """Edit Student Info and Reset Passwords"""
        try:
            if 'password' in kwargs:
                kwargs['password'] = self.auth.hashpassword(kwargs['password'])
                self.db.update_record(table='user',**kwargs)
                return {'success': True, 'message': 'Password Reset Successful'}
            else:
                self.db.update_record(table='user',**kwargs)
                return {'success': True, 'message': 'Update Successful'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        

    def delete(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"