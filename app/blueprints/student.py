from flask import Flask, Blueprint, jsonify

class Student():
    def __init__(self,idno:str,fullname:str,course:str, year:int):
        self.idno = idno
        self.fullname = fullname
        self.course = course
        self.year = year
    
    def get_idno(self):                 return self.idno
    def get_fullname(self):             return self.fullname
    def get_course(self):               return self.course
    def get_year(self):                 return self.year
    
    def to_dict(self):
        """Convert the Student object to a dictionary for JSON response."""
        return {
            "idno": self.idno,
            "fullname": self.fullname,
            "course": self.course,
            "year": self.year
        }
    def __str__(self):
        return f"Student ID: {self.idno}\nName: {self.get_fullname()}\nCourse: {self.course}\nYear: {self.year}"
    
# Define a Blueprint for student-related routes
student_bp = Blueprint('student', __name__)