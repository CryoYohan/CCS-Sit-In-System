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
    
    def retrieve_all_announcements(self):
        """Retrieve all announcements"""
        try:
            announcements = self.db.getall_records(table='announcement')
            return{'success':True, 'announcements':announcements}
        
        except Exception as e:
            return {'erorr':str(e)}
    