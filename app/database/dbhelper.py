from sqlite3 import connect, Row

class Databasehelper:
    def __init__(self) -> None:
        self.database = 'user.db'

    def getdb_connection(self):
        """Establishes and returns a database connection."""
        connection = connect(self.database)
        connection.row_factory = Row  # Ensures results are returned as dictionaries
        return connection

    def getprocess(self, sql: str, params=()):
        """Executes a SELECT query and returns results."""
        connection = self.getdb_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def postprocess(self, sql: str, params=()):
        """Executes an INSERT, UPDATE, or DELETE query."""
        connection = self.getdb_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
        row_count = cursor.rowcount
        cursor.close()
        connection.close()
        return row_count > 0  # Returns True if at least one row is affected

    def getall_records(self, table: str) -> list:
        """Retrieves all records from a specified table."""
        query = f"SELECT * FROM {table}"
        return self.getprocess(query)
    
    def get_all_announcements(self):
        """Retrieves all records from announcement table with order by date."""
        query = f"SELECT * FROM announcement ORDER BY date_posted DESC"
        return self.getprocess(query)
    
    def find_announcement(self, post_id: str):
        """Finds a specific announcement by post_id."""
        sql = f"SELECT * FROM announcement WHERE post_id = ?"
        return self.getprocess(sql, (post_id,))
    
    def get_all_users(self)->list:
        """Retrieves all records from a specified table."""
        query = f"SELECT * FROM user WHERE role <> 'Admin'"
        return self.getprocess(query)

    def getall_records_rolebased(self,role:str)->list:
        """Retrieves all staff"""
        query = "SELECT * FROM user WHERE role = ? ORDER BY lastname"
        return self.getprocess(query, (role,))


    def getall_sitinrecords(self)->list:
        """Retrieve all sit-in records"""
        query = "SELECT * FROM sitin_record_details"
        return self.getprocess(query)
    
    def retrieve_all_students_to_sitin(self):
        """ Retrieve all students joined sitin reservation"""
        query = f"SELECT DISTINCT * FROM students_to_sitin ORDER BY lastname ASC"
        return self.getprocess(query)

    def retrieve_all_current_sitins(self):
        """ Retrieve all students who currently in lab"""
        query = "SELECT * FROM user WHERE status = 'In-lab'"
        return self.getprocess(query)

    def getall_sessionhistory(self, idno:str)->list:
        """Retrieve session history"""
        query = f"SELECT * FROM sitin_record WHERE idno = ? ORDER BY status DESC"
        return self.getprocess(query, (idno,))
    
    def reset_all_session(self):
        """Retrieve session history"""
        query = f"UPDATE user SET session = 30 WHERE role = 'Student'"
        return self.getprocess(query)
    
    def getall_feedbacks(self, idno)->list:
        query = f"SELECT * FROM student_feedback WHERE idno = ? ORDER BY submitted_on DESC"
        return self.getprocess(query, (idno),)

    def getone_feedback(self, feedback_id):
        """Retrieve one feedback"""
        query = f"SELECT * FROM student_feedback WHERE feedback_id = ?"
        return self.getprocess(query, (feedback_id,))
    
    def get_student_reservation_history(self,idno)->list:
        """Retrieve Student Reservation History"""
        query = f"SELECT * FROM reservation WHERE idno = ?"
        return self.getprocess(query, (idno,))

    def find_record(self, table: str, idno: str):
        """Finds a specific record by idno."""
        sql = f"SELECT * FROM {table} WHERE idno = ?"
        return self.getprocess(sql, (idno,))
    
    def fetchOne(self, table, **kwargs):
        """Fetches a single record based on the specified column and value."""
        if not kwargs:
            raise ValueError("At least one filter condition must be provided")
        
        # Get the first key-value pair from kwargs
        column, value = next(iter(kwargs.items()))
        
        sql = f"SELECT * FROM {table} WHERE {column} = ?"
        print(sql)
        return self.getprocess(sql, (value,))
    
    def deleteOne(self, table, column, value):
        """Delete one record dynamic"""
        sql = f"DELETE FROM {table} WHERE {column} = ?"
        return self.postprocess(sql, (value,))
    
    def fetchLabPurpose(self, table, lab_name, reason):
        """Fetches a single record based on the specified column and value."""
        sql = f"SELECT * FROM {table} WHERE lab_name = ? AND reason = ?"
        return self.getprocess(sql, (lab_name,reason,))

    def fetchAll(self, table):
        """Fetches all records from the specified table."""
        sql = f"SELECT * FROM {table}"
        return self.getprocess(sql)
    

    def find_reservation_record(self,idno:str):
        """Finds a specific reservation record by idno."""
        sql = f"SELECT * FROM reservation WHERE idno = ? AND status = 'Pending'"
        return self.getprocess(sql, (idno,))
    
    def find_reservation_info(self, reservation_id: str):
        """Finds a specific record by reservation_id."""
        sql = f"SELECT * FROM student_reservations_info WHERE reservation_id = ?"
        return self.getprocess(sql, (reservation_id,))
    
    def get_reservations_by_status(self, status):
        """Fetch reservations by status"""
        query = "SELECT * FROM reservation WHERE status = ?"
        return self.getprocess(query, (status,))

    def add_record(self, table:str, **kwargs):
        """Adds a new record to a table."""
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?" for _ in kwargs])
        values = tuple(kwargs.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.postprocess(sql, values)

    def update_record(self, table:str, **kwargs):
        """Updates an existing record in a table."""
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        if len(keys) < 2:
            return False  # Ensures there's at least one field to update

        set_clause = ", ".join([f"{key} = ?" for key in keys[1:]])
        sql = f"UPDATE {table} SET {set_clause} WHERE {keys[0]} = ?"

        return self.postprocess(sql, values[1:] + [values[0]])  # Moves ID to the end

    def delete_record(self, table: str, **kwargs):
        """Deletes a record based on the given criteria."""
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        sql = f"DELETE FROM {table} WHERE {keys[0]} = ?"
        return self.postprocess(sql, (values[0],))
