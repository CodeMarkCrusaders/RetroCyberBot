from discord import Interaction
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from Data_classes.character import Character
from Data_classes.memcell import MemoryCell
from Data_classes.Data_user import User
#from screen import Screen

class Base:

    def __init__(self ,screen):

        self.Screen = screen
        self.User:User = self.Screen.ControlUser
        self.Character: Character = self.User.SelectedCharacter
        self.Data: MemoryCell

        
    async def СhooseMeaning(self, interation: Interaction):

        NameMeaning = interation.data["custom_id"]

        self.Data.СhooseMeaning(NameMeaning = NameMeaning)

        await interation.response.edit_message()

    async def SetMeaning(self, interation: Interaction):

        if 'values' in  interation.data.keys():

            Value = interation.data["values"][0]

        else:

            Value = interation.data['custom_id']

        self.Data.SetMeaning(Value)

        await self.Update(interation)

    async def СhooseSetMeaning(self, interation: Interaction):

        if 'values' in  interation.data.keys():

            Data = interation.data["values"][0].split('!')

        else:

            Data = interation['custom_id'].split('!')

        self.Data.ChooseSetMeaning(NameMeaning = Data[0], Value = Data[1])

        await self.Update(interation)

    async def Transition(self, interation: Interaction):

        MethodName = None

        if 'values' in  interation.data.keys():

            MethodName = interation.data['values'][0]

        else:

            MethodName = interation.data["custom_id"]

        if MethodName == 'back':

            await self.Screen.Back()

        else:

            if MethodName == 'menu':

                self.User.Save()

            await self.Screen.Show(MethodName)

        await interation.response.edit_message(embed = self.Screen.Embed, view = self.Screen)

    async def Update(self, interation: Interaction):    

        await self.Screen.Update()

        await interation.response.edit_message(embed = self.Screen.Embed, view = self.Screen)

