from .user import User

class Student(User):
    def __init__(self,idno:str,firstname:str, middlename,lastname,course:str, year:int, email:str,image:str,role="Student"):
        super().__init__(idno, firstname, middlename,lastname, email)
        self.idno = idno
        self.course = course
        self.year = year
        self.role = role
        self.image = image
    
    def add_reservation(self, reservation):
        pass  

    def delete_reservation(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"
    
    
# Define a Blueprint for student-related routes
# student_bp = Blueprint('student', __name__)