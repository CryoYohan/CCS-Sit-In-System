from .user_mgt_module.student import Student
class Record():
    def __init__(self, student:Student, timein:str,timeout:str,duration:float,remaining_session:float, reason:str):
        self.student = student
        self.timein = timein
        self.timeout = timeout
        self.duration = duration
        self.remaining_session = remaining_session
        self.reason = reason

    def get_datetime(self):             return self.datetime
    def get_reason(self):               return self.reason
    def get_student(self):              return self.student
    
    def __str__(self):
        return f"{self.student.get_fullname()} - {self.datetime} - {self.reason}"