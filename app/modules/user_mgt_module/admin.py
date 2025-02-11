from .user import User

class Admin(User):
    def __init__(self,idno:str, firstname:str, middlename:str, lastname:str, email:str,image:str, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role
        self.image = image

    def add(self):
        pass

    def delete(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"