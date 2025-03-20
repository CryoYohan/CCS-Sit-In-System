from .user import User

class Student(User):
    def __init__(self,idno:str,firstname:str, middlename,lastname,course:str, year:int, email:str,image:str,session:int,role="Student"):
        super().__init__(idno, firstname, middlename,lastname, email)
        self.idno = idno
        self.course = course
        self.year = year
        self.role = role
        self.image = image
        self.session = session
    
    def add_reservation(self, reservation):
        pass  

    def delete_reservation(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"
    
    def get_announcements_for_student(self):
        """Retrieve all announcements"""
        try:
            announcements = self.retrieve_all_announcements()
            return{'success':True, 'data':announcements['data']}
        
        except Exception as e:
            return {'erorr':str(e)}
    
    def upload_profile_icon(self,profile_icon,student):
        """Upload profile icon"""
        try:
            self.db.update_record(table='user',idno=self.idno, image=profile_icon)
            student.image = profile_icon
            return {'success':True, 'student':student}
        except Exception as e:
            return {'success':False, 'error':str(e)}
    