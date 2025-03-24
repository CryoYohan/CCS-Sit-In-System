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
            # Fetch all reservations for the student
            student_reservations = self.db.find_record('reservation', idno=kwargs.get('idno'))
            print("All Reservations:", student_reservations)  # Debugging

            # Check if the student has any Pending or Approved reservations
            active_reservations = [
                reservation for reservation in student_reservations
                if reservation['status'] in ['Pending', 'Approved']  # Access 'status' directly
            ]
            print("Active Reservations:", active_reservations)  # Debugging

            if active_reservations:
                return {'success': False, 'message': 'You already have an active reservation. Cancel it to reserve again.'}
            else:
                # Add the new reservation
                self.db.add_record(table='reservation', **kwargs)
                return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        

    def cancel_reservation(self, **kwargs):
        """Cancel a reservation"""
        print(f"RESERVATION ID FROM KWARGS {kwargs.get('reservation_id')}")
        try:
            # Fetch the reservation to cancel
            reservation = self.db.find_reservation(reservation_id=kwargs.get('reservation_id'))
            print("Reservation to Cancel:", reservation)  # Debugging

            if not reservation:
                return {'success': False, 'message': 'Reservation not found.'}
            else:
                # Update the reservation status to 'Cancelled'
                self.db.update_record(
                    table='reservation',
                    reservation_id=kwargs.get('reservation_id'),
                    status='Cancelled'
                )
                return {'success': True}
        except Exception as e:
            print("Error canceling reservation:", e)  # Debugging
            return {'success': False, 'error': str(e)}


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
        

    def retrieve_reservations_by_status(self, status):
        """Retrieve all reservations by status"""
        try:
            # Fetch reservations by status from the database
            reservations = self.db.get_reservations_by_status(status=status)
            return {'success': True, 'data': reservations}

        except Exception as e:
            # Log the error for debugging
            print(f"Error in retrieve_reservations_by_status: {str(e)}")
            return {'success': False, 'message': 'An error occurred while fetching reservations.'}
    