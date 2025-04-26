from .user import User
from ..security.hashpw import PasswordHashing
from random import choice
from datetime import datetime

class Admin(User):
    auth = PasswordHashing()
    def __init__(self,idno:str, firstname:str, middlename:str, lastname:str, email:str,image:str, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role
        self.image = image

    def add_staff(self,**kwargs):
        """Add a new Staff"""
        password = kwargs.get("password")
        kwargs['password'] = self.auth.hashpassword(password)
        kwargs['image'] = choice(self.profileicons)

        print(f'Data to insert to table{kwargs}')
        
        try:
            self.db.add_record(table='user',**kwargs) 
            del kwargs['password']
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def retrieve_all_staff(self):
        """Retrieve all staff"""
        return self.db.getall_records_rolebased(role='Staff')

    def retrieve_all_students(self):
        """Retrieve all students"""
        return self.db.getall_records_rolebased(role='Student')

    
    def retrieve_all_users(self):
        """Retrieve all users"""
        return self.db.get_all_users()

    def retrieve_all_labs(self):
         """Retrieve all labs"""
         return self.db.getall_records(table='lab')

    def add_lab(self, **kwargs):
        """Add a lab"""
        try:
            kwargs['add_date'] = datetime.now()
            self.db.add_record(table='lab',**kwargs) 
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def edit_lab(self,**kwargs):
        """Edit lab"""
        try:
            print('HEY')
            kwargs['add_date'] = datetime.now()
            self.db.update_record(table='lab', **kwargs)
            return {
                'success':True
            }
        except Exception as e:
            print('HOY')
            return {
                'success':False,
                'error': str(e)
            }

    def delete_lab(self,lab_id):
        """Delete Lab"""
        try:
            self.db.deleteOne(table='lab', column='lab_id', value=lab_id)
            return {
                'success':True
            }
        except Exception as e:
            return {'success':False, 'error': str(e)}

    def get_lab_details(self, lab_id):
        """Get lab by ID"""
        try:
            lab = self.db.fetchOne(table='lab',lab_id=lab_id)
            return {
                'success':True,
                'data': lab
            }
        except Exception as e:
            return {'success':False, 'error': str(e)}
        
    def retrieve_all_current_sitins(self):
        """ Retrieve all students who currently in lab"""
        return self.db.retrieve_all_current_sitins()
    
    def retrieve_all_pending_reservations(self):
        """Retrieve all reservations"""
        return self.db.get_reservations_by_status(status='Pending')

    def retrieve_all_feedbacks(self):
        """Retrieve all feedbacks"""
        try:
            feedbacks = self.db.getall_feedbacks_admin()
            return {
                'success': True, 'data': feedbacks
            }
        except Exception as e:
            return {
                'success': False, 'message': str(e)
            }
    
    def retrieve_one_feedback(self, feedback_id):
        """Retrieve one feedback"""
        try:
            feedback = self.db.getone_feedback(feedback_id=feedback_id)
            return {
                'success': True, 'data': feedback
            }
        except Exception as e:
            return {
                'success': False, 'message': str(e)
            }

    def get_announcements_for_students(self):
        """Retrieve all announcements from DB"""
        try:
            announcements = self.retrieve_all_announcements()
            return{'success':True, 'data':announcements['data']}

        except Exception as e:
            return {'success': False, 'message': str(e)}


    def add_announcement(self, **kwargs):
        """Add an announcement"""
        try:
            self.db.add_record(table='announcement',**kwargs) 
            return {'success': True} 
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
    def get_announcement(self, post_id):
        """Get a specific announcement"""
        try:
            announcement = self.db.find_announcement(post_id=post_id)
            return {'success': True, 'data': announcement}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def delete_announcement(self,post_id):
        """Delete a announcement"""
        try:
            self.db.delete_record(table='announcement', post_id=post_id)
            print('Deleted the announcement')
            return {'success': True}
        except Exception as e:
            print(f'Cannot Delete the announcement\n{str(e)}')
            return {'success': False, 'message': str(e)}
        
    def update_announcement(self, **kwargs):
        """Update an announcement"""
        try:
            self.db.update_record(table='announcement',**kwargs)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    
    def retrieve_all_sitinrecords(self):
        """Retrieve all Joined Sitin Records"""
        try:
            records = self.db.fetchAll(table='sitin_record_details')
            return {'success':True, 'data':records}
        except Exception as e:
            return {'success':False, 'error':str(e)}

    
    def retrieve_sitinrecord_by_lab(self, lab_name):
        """Retrieve all Joined Sitin Records by lab_id"""
        try:
            records = self.db.fetchOne(table='sitin_record_details', lab_name=lab_name)
            return {'success': True, 'data': records}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    def retrieve_sitinrecord_by_purpose(self, reason):
        """Retrieve all Joined Sitin Records by purpose"""
        try:
            records = self.db.fetchOne(table='sitin_record_details', reason=reason)
            return {'success': True, 'data': records}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    def retrieve_sitinrecord_by_lab_and_purpose(self, lab_name, reason):
        """Retrieve all Joined Sitin Records by lab_id and purpose"""
        try:
            records = self.db.fetchLabPurpose(table='sitin_record_details', lab_name=lab_name, reason=reason)
            print('LAB AND REASON retrieval')
            return {'success': True, 'data': records}
        except Exception as e:
            print('Caught error in retrieve by lab and reason')
            return {'success': False, 'message': str(e)}
    
    def approve_reservation(self,reservation_id,admin):
        """Approve a reservation"""
        try:
            reservation = self.db.find_reservation_info(reservation_id=reservation_id)
            today = datetime.now()
            message = f'Hey {reservation[0]["firstname"]}! Your reservation has been approved. Please proceed to the lab at {reservation[0]["lab_id"]} on {reservation[0]["reserve_date"]}.'
            self.db.update_record(table='reservation',reservation_id=reservation_id,status='Approved',message=message, staff_idno=admin.idno, approved_on=today)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': f'Approving Reservation ERRROR: {str(e)}'}
    
    def decline_reservation(self, reservation_id,admin):
        """Decline a reservation"""
        try:
            reservation = self.db.find_reservation_info(reservation_id=reservation_id)
            message = f'Hey {reservation[0]["firstname"]}! Your reservation has been declined. Please contact the lab staff for more information.'
            self.db.update_record(table='reservation',reservation_id=reservation_id,status='Denied',message=message, staff_idno=admin.idno)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': f'Declining Reservation ERRROR: {str(e)}'}

    
    def sit_in_student(self,**kwargs):
        """Sit in a student"""
        sitin_datetime = datetime.now()
        kwargs['sitin_in'] = sitin_datetime

        update_student_status = {
            'idno': kwargs.get('idno'),
            'status': 'In-lab',
        }

        try:
            self.db.add_record(table='sitin_reservation',**kwargs)
            self.db.update_record(table='user',**update_student_status)
            return {'success':True}
        except Exception as e:
            return {'success':False, 'error':str(e)}

    def logoff_student(self, idno,staff_idno):
        """Log-off student"""
        try:
            print(f'IDNO: {idno}')
            reservation = self.db.find_record(table='current_sitin',idno=idno)
            user = self.db.find_record(table='user', idno=idno)

            data={
                    'reservation_id': reservation[0]['reservation_id'],
                    'idno': reservation[0]['idno'],
                    'lab_id': reservation[0]['lab_id'],
                    'sitin_in': reservation[0]['sitin_in'],
                    'sitin_out': datetime.now(),  # Log the current time
                    'staff_idno': reservation[0]['staff_idno'],
                    'logged_off_by': staff_idno,  # Admin/Staff who logs off the student
                    'status': 'Completed',
                    'reason': reservation[0]['reason'],
                    'completed_at': datetime.now()
            }
            
            # Insert into sitin_record with the correct log-off time and logged_off_by
            self.db.add_record(
                table='sitin_record',
                **data
            )

            update_status_session = {
                'idno' : idno,
                'session': user[0]['session']-1,
                'status': 'Idle'
            }

            self.db.update_record(table='user',**update_status_session)
            print('successfully logged off the student')
            return {'success': True}
        except Exception as e:
            print(f'failed logged off the student{str(e)}')
            return {'success': False, 'message': str(e)}
        

    def add_lab_resource(self, **kwargs):
        """Add lab resource"""
        try:
            self.db.add_record(table='lab_resources',**kwargs)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_lab_resource(self, resources_id):
        """Delete lab resource"""
        try:
            self.db.delete_record(table='lab_resources', resources_id=resources_id)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
    def update_lab_resource(self, **kwargs):
        """Edit lab resource"""
        try:
            self.db.update_record(table='lab_resources', **kwargs)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_lab_resources(self):
        """Get lab resources"""
        try:
            resources = self.db.getall_records(table='lab_resources')
            return {'success': True, 'data': resources}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_lab_resource_by_id(self, resources_id):
        """Get lab resource by ID"""
        try:
            resource = self.db.fetchOne(table='lab_resources',resources_id=resources_id)
            return {'success': True, 'data': resource}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def publish_unpublish(self, **kwargs):
        """Publish/Unpublish lab resources"""
        try:
            self.db.update_record(table='lab_resources', **kwargs)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}


    def update(self, **kwargs):
        """Edit Student Info and Reset Passwords"""
        try:
            if 'password' in kwargs:
                kwargs['password'] = self.auth.hashpassword(kwargs['password'])
                self.db.update_record(table='user',**kwargs)
                return {'success': True, 'message': 'Password Reset Successful'}
            else:
                self.db.update_record(table='user',**kwargs)
                return {'success': True, 'message': 'Update Successful'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    
    def reset_one_session(self, idno):
        """Reset one session"""
        try:
            user = self.db.find_record(table='user', idno=idno)
            if user:
                self.db.update_record(table='user', idno=idno, session=30)
                return {'success': True}
            else:
                return {'success': False, 'message': 'User not found'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    def reset_all_sessions(self):
        """Reset all sessions"""
        try:
            ok = self.db.reset_all_session()
            if ok:
                return {'success': True}
            else:
                return {'success': False, 'message': 'Failed to reset sessions'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def reset_password(self, idno, password):
        """Reset password"""
        try:
            hashed_password = self.auth.hashpassword(password)
            self.db.update_record(table='user', idno=idno, password=hashed_password)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        

    def add_points(self, idno, points):
        """Add points to a student"""
        try:
            user = self.db.fetchOne(table='user', idno=idno)
            if user:
                new_points = user[0]['points'] + int(points)
                self.db.update_record(table='user', idno=idno, points=new_points)
                print('Successfully added points')
                return {'success': True}
            else:
                print('have not added points')
                return {'success': False, 'error': 'User not found'}

        except Exception as e:
            print(f'Error caught {str(e)}')
            return {'success':False, 'error': str(e)}
        
    def update_computer_slots(self, lab_id, update_index, status):
        """Update computer slots"""
        try:
            lab = self.db.find_record(table='lab', lab_id=lab_id)
            if not lab:
                return {'success': False, 'message': 'Lab not found'}
            
            computers_list:list = list(lab[0]['computers'])

            if len(computers_list) != len(update_index):
                return {'success': False, 'message': 'Mismatch in computer slots length'}
            
            computers_list[update_index] = status

            updated_computers = ''.join(computers_list)

            self.db.update_record(table='lab', lab_id=lab_id, computers=updated_computers)
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def find_lab(self,lab_id):
        """Find a lab"""
        try:
            lab = self.db.fetchOne(table='lab', lab_id=lab_id)
            if lab:
                print('Retrieve Find Lab success!')
                return {'success': True, 'data': lab}
            else:
                print('Retrieve Find Lab fail!')
                return {'success': False, 'message': 'Lab not found'}
        except Exception as e:
            print(f'Retrieve Find Lab Catch error! LAB ID {lab_id}')
            return {'success': False, 'error': str(e)}

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"