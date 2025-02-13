from .user import User

class Admin(User):
    def __init__(self,idno:str, firstname:str, middlename:str, lastname:str, email:str,image:str, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role
        self.image = image

    def add_staff(self,staff_data):
        hashed_password = ""

        password = staff_data.pop('password',None)
        confirmpassword = staff_data.pop('confirm_password',None)

        if password and password != confirmpassword:
            return {"success": False, "error": "Passwords do not match"}

        add_data = {
            "idno": staff_data.get("idno"),
            "firstname": staff_data.get("firstname"),
            "middlename": staff_data.get("middlename"),
            "lastname": staff_data.get("lastname"),
            "course": staff_data.get("course"),
            "year":staff_data.get("year"),
            "email": staff_data.get("email"),
        }

        # Hash password
        if password:
            hashed_password = self.auth.hashpasword.hashpassword(password)
            add_data['password'] = hashed_password
        
        try:
            response = self.auth.user_is_registered(**{k:v for k,v in add_data.items() if v},url='staff')

            del add_data['password']
            if response['success']:
                return {'success': True}

            else:
                return {'success' : False, 'error':response['error']}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


    def delete(self):
        pass

    def __str__(self):
        return f"{self.firstname.title()} {self.middlename[0].capitalize()}. {self.lastname.title()}"