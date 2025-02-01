from student import Student
class Record():
    def __init__(self, student:Student, datetime:str, reason:str):
        self.student = student
        self.datetime = datetime
        self.reason = reason

    def get_datetime(self):             return self.datetime
    def get_reason(self):               return self.reason
    def get_student(self):              return self.student
    
    def __str__(self):
        return f"{self.student.get_fullname()} - {self.datetime} - {self.reason}"