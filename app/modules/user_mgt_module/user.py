from ...database.dbhelper import Databasehelper
from random import choice

class User():
    db = Databasehelper()
    table = 'user'
    profileicons = ['bear.png','cat.png','chicken.png', 'meerkat.png','panda.png','polar-bear.png', 'shark.png','weasel.png']
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

    def delete(self):
        pass

    def random_profile(self)->str:
        return choice(self.profileicons)
