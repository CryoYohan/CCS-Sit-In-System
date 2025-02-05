from .user import User


class Student(User):
    def __init__(self,idno:str,firstname:str, middlename,lastname,course:str, year:int, email:str, role="Student"):
        super().__init__(idno, firstname, middlename,lastname,course,year, email, role="Student")
        self.idno = idno
        self.course = course
        self.year = year
        self.role = role
    
    def add_reservation(self, reservation):
        pass  

    def delete_reservation(self):
        pass
    
    
# Define a Blueprint for student-related routes
# student_bp = Blueprint('student', __name__)