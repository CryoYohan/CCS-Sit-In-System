from .user import User

class Staff(User):
    def __init__(self, idno, firstname, middlename, lastname, email,course,year, role="Staff"):
        super().__init__(idno,firstname,middlename,lastname,email)
        self.role = role    
        self.course = course
        self.year = year
    def add_student_to_lab():
        pass

    def remove_student_from_lab():
        pass

    def restart_session():
        pass