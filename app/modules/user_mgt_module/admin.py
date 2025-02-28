from .user import User
from ..security.hashpw import PasswordHashing
from random import choice

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
    
    def retrieve_all_users(self):
        """Retrieve all users"""
        return self.db.get_all_users()


    def add_announcement(self, **kwargs):
        """Add an announcement"""
        try:
            self.db.add_record(table='announcement',**kwargs) 
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def retrieve_all_announcements(self):
        """Retrieve all announcements"""
        try:
            announcements = self.db.getall_records(table='announcement')
            return{'success':True, 'announcements':announcements}
        
        except Exception as e:
            return {'erorr':str(e)}
    
    def retrieve_all_sitinrecords(self):
        """Retrieve all Joined Sitin Records"""
        try:
            sitinrecords = self.db.getall_sitinrecords(idno=None)
            return{'success':True, 'sitinrecords':sitinrecords}
        
        except Exception as e:
            return {'erorr':str(e)}


    def delete(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"