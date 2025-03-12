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
    
    def get_all_users(self)->list:
        """Retrieves all records from a specified table."""
        query = f"SELECT * FROM user WHERE role <> 'Admin'"
        return self.getprocess(query)

    def getall_records_rolebased(self,role:str)->list:
        """Retrieves all staff"""
        query = f"SELECT * FROM user WHERE role = '{role}' ORDER BY lastname"
        return self.getprocess(query)


    def getall_sitinrecords(self, idno:str)->list:
        """Retrieve all records joined from user table and lab table"""
        if not idno == None:
            query = f"SELECT sr.reservation_id, l.lab_name, sr.idno, u.firstname, sr.status, sr.sitin_in, sr.sitin_out, sr.staff_idno FROM sitin_reservation sr JOIN user u ON u.idno =  sr.idno JOIN lab l ON l.lab_id = sr.lab_id WHERE sr.idno = ?"
            return self.getprocess(query, (idno,))
        else:
            query = f"SELECT * FROM students_with_status_sitin_reserve"
            return self.getprocess(query)
    
    def retrieve_all_students_to_sitin(self):
        """ Retrieve all students joined sitin reservation"""
        query = f"SELECT * FROM students_to_sitin"
        return self.getprocess(query)
    
    def retrieve_all_current_sitins(self):
        """ Retrieve all students who currently in lab"""
        query = "SELECT * FROM current_sitin"
        return self.getprocess(query)

    def getall_sessionhistory(self, idno:str)->list:
        """Retrieve session history"""
        query = f"SELECT sr.sitin_out, l.lab_name, sr.status, sr.sitin_out FROM sitin_reservation sr JOIN lab l ON l.lab_id = sr.lab_id WHERE sr.idno = ? AND sr.status= 'Completed'"
        return self.getprocess(query, (idno,))

    def find_record(self, table: str, idno: str):
        """Finds a specific record by idno."""
        sql = f"SELECT * FROM {table} WHERE idno = ?"
        return self.getprocess(sql, (idno,))

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
