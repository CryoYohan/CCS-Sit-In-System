from ...database.dbhelper import Databasehelper
class Reservation():
    db = Databasehelper()
    table_lab = 'lab'
    table_reserve = 'sitin_reservation'
    def add_sitin_details(self,lab_id, idno,reason, sitin_datetime=None, sitinout_datetime=None, staff_idno=None,status='Pending'):
        try:
            self.db.add_record(
                                table=self.table_reserve,
                                lab_id=lab_id, idno=idno,
                                reason=reason, 
                                sitin_in=sitin_datetime, 
                                sitin_out=sitinout_datetime,
                                staff_idno=staff_idno,status=status,
                            )
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error':str(e)}

    def confirm_sitin(self):
        pass

    def deny_sitin(self):
        pass
    
    def retrieve_labs(self)->list:
        """Retrieve all labs"""
        return self.db.getall_records(table=self.table_lab)

    def retrieve_lab_id(self, lab_name):
        """Retrieve lab id using UNIQUE lab name shet"""
        labs = self.db.getall_records(table=self.table_lab)
        lab_id:int = 0
        for lab in labs:
            if lab['lab_name'] == lab_name:
                lab_id = lab['lab_id']
        return lab_id

    def retrieve_sitinrecords(self, idno:str):
        """Retrieve all sitin records"""
        return self.db.getall_sitinrecords()

    def retrieve_sessionhistory(self, idno:str):
        """Retrieve all session history"""
        return self.db.getall_sessionhistory(idno=idno)
    
    def request_reservation(self, **kwargs):
        """Request a reservation"""
        try:
            already_reserved = self.db.find_record('reservation', kwargs.get('idno'))
            if already_reserved:
                return {'success':False, 'message': 'You already made a reservation. Cancel current reservation to reserve again.'}
            else:
                self.db.add_record(table='reservation', **kwargs)
                return {'success':True}
        except Exception as e:
            return {'success':False, 'error':str(e)}

    def retrieve_reservation_history(self, idno):
        """Retrieve all reservation history for a student"""
        try:
            if not idno:
                return {'success': False, 'message': 'Student ID (idno) is required.'}

            # Fetch reservation history from the database
            reservations = self.db.get_student_reservation_history(idno=idno)
            return {'success': True, 'data': reservations}

        except Exception as e:
            # Log the error for debugging
            print(f"Error in retrieve_reservation_history: {str(e)}")
            return {'success': False, 'message': 'An error occurred while fetching reservation history.'}
    