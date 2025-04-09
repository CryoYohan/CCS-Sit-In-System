from .user import User
from datetime import datetime


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


    def retrieve_student_sessions_history(self,idno:str):
        """Retrieve all student sessions"""
        try:
            session_history =  self.db.getall_sessionhistory(idno=idno)
            return {
                'success':True,
                'data': session_history,
            }
        except Exception as e:
            return {'success':False, 'error':str(e)}

    def request_reservation(self, **kwargs):
        """Request a reservation"""
        try:
            already_reserved = self.db.find_reservation_record(idno=kwargs.get('idno'))
            if already_reserved:
                return {'success':False, 'error': 'You already made a reservation. Cancel current reservation to reserve again.'}
            else:
                self.db.add_record(table='reservation', **kwargs)
                return {'success':True}
        except Exception as e:
            return {'success':False, 'error':str(e)}

    def send_feedback(self,**kwargs):
        """Send feedback"""
        try:
            kwargs['submitted_on'] = datetime.now()
            self.db.add_record(table='feedback', **kwargs)
            return {'success':True}
        except Exception as e:
            return {'success':False, 'error':str(e)}
    
    def retrieve_my_feedbacks(self, idno):
        """Retrieve Student Feedbacks"""
        try:
            my_feedbacks = self.db.getall_feedbacks(idno=idno)
            return {'success': True, 'data':my_feedbacks}
        except Exception as e:
            return {'success': False, 'message':str(e)}
    
    def get_lab_resources(self):
        """Retrieve all lab resources"""
        try:
            lab_resources = self.db.fetchOne(table='lab_resources', status='Published')
            return {'success': True, 'data': lab_resources}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    