from ...database.dbhelper import Databasehelper

class User():
    def __init__(self, idno,firstname,middlename,lastname,email):
        self.db = Databasehelper()
        self.table = "user"
        self.idno = idno
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email

    def add(self):
        pass

    def update(self):
        pass

    def edit(self, firstname=None,middlename= None, lastname=None, email=None, course=None,year=None):
        """Allows user to edit only specified fields."""
        update_data = { 
            "idno": self.idno,
            "firstname": firstname, 
            "middlename": middlename,
            "lastname": lastname, 
            "email": email, 
            "course": course,
            "year": year
        }
        # Remove fields that are None (not edited)
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return "No changes made."

        return self.db.update_record(self.table, self.idno, **update_data)

    def delete(self):
        pass