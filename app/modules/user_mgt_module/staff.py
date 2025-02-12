from .user import User

class Staff(User):
    def __init__(self, idno:str, firstname:str, middlename:str, lastname:str, image:str, email:str,course:str=None,year:int=None, role="Staff"):
        super().__init__(idno,firstname,middlename,lastname,email)
        self.role = role    
        self.course = course
        self.year = year
        self.image = image
    def add_student_to_lab():
        pass

    def remove_student_from_lab():
        pass

    def restart_session():
        pass

    def __str__(self):
        return f"{self.firstname} {self.middlename[0].upper()}. {self.lastname}"