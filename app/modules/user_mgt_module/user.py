from ...database.dbhelper import Databasehelper
from ..login_register_module import Authorization

class User():
    profileicons = ['bear.png','cat.png','chicken.png', 'meerkat.png','panda.png','polar-bear.png', 'shark.png','weasel.png','wolf.png']
    db = Databasehelper()
    table = 'user'
    auth = Authorization()
    def __init__(self, idno,firstname,middlename,lastname,email):
        self.idno = idno
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email

    def add(self):
        pass

    def update(self):
        pass

    def edit(self,**kwargs):
        """Allows user to edit only specified fields."""
        if not kwargs:
            return "No changes made."

        self.db.update_record(self.table,**kwargs)  # Update only provided fields
    
    def retrieve_all_announcements(self):
        """Retrieve all announcements"""
        try:
            announcements = self.db.getall_records(table='announcement')
            return{'success':True, 'announcements':announcements}
        
        except Exception as e:
            return {'erorr':str(e)}

    def delete(self):
        pass

    def random_profile(self)->str:
        return choice(self.profileicons)
