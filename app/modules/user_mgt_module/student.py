from flask import Flask, Blueprint
from .user import User


class Student(User):
    def __init__(self,idno:str,fullname:str,course:str, year:int):
        super().__init__()
        self.idno = idno
        self.fullname = fullname
        self.course = course
        self.year = year
    
    def add_reservation(self, reservation):
        pass  
    
    
# Define a Blueprint for student-related routes
# student_bp = Blueprint('student', __name__)