from .user import User

class Admin(User):
    def __init__(self,idno:str, firstname:str, middlename:str, lastname:str, email:str,image:str, role="Admin"):
        super().__init__(idno, firstname, middlename, lastname, email)
        self.role = role
        self.image = image

    def add_staff(self,**kwargs):
        hashed_password = ""
        password = kwargs.get("password")

        # Hash password
        if password:
            hashed_password = self.auth.hashpasword.hashpassword(password)
            kwargs['password'] = hashed_password
        
        try:
            response = self.auth.user_is_registered(**{k:v for k,v in kwargs.items() if v},url='staff')

            del kwargs['password']
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