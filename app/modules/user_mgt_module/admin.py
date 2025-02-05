from .user import User

class Admin(User):
    def __init__(self,idno, firstname, middlename,lastname, email, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role

    def add(self):
        pass

    def delete(self):
        pass
