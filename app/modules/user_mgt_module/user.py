from ..database.dbhelper import Databasehelper

class User():
    def __init__(self):
        self.db = Databasehelper()

    def edit_profile(self, **kwargs):
        pass