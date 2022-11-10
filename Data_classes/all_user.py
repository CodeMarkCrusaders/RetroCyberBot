
from .Data_user import User
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from screen import Screen

class Data_all_user():
    
    def __init__(self):

        self.all_user = {}
        self.all_character = {}

    def Availability(self , id: str) -> Screen:


        if id in self.all_user.keys():

            screen = self.all_user[id]


        else:

            user = User(id)

            screen = Screen(user)

            self.all_user[id] = screen

        return screen
    
AllUser = Data_all_user()

