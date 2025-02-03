from .user import User

class Admin(User):
    def __init__(self):
        super().__init__()

    def add_user(self):
        self.db.add_record('admin',idno=idno,fullname=fullname,course=course,year=year,email=email,password=hashed_password)