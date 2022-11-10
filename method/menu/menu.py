import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import View,Select, Button
from discord import ButtonStyle, Embed, Interaction
from method.menu.options import list_character
#from screen import screen

class menu:

    __name__ = "menu"
    def __init__(self, screen) -> None:

        self.screen = screen
        self.User = self.screen.ControlUser
        self.screen.Embed = Embed ( title = 'Главное меню.\nЧто пожелаете делать?' )
        self.screen.ScreenName = 'menu'
    
        Character_Select = Select(
            placeholder = 'Выберите персонажа',
            options = list_character(self.screen.ControlUser),
            row = 0,
        )
        Character_Select.callback = self.load_callback
        self.screen.add_item(Character_Select)
    
        button_new = Button(
            label= "Новый персонаж" ,
            style = ButtonStyle.gray,
            row = 4
        )
        button_new.callback = self.new_callback
        self.screen.add_item(button_new)

    async def load_callback(self,interation : Interaction):
        
        data = interation.data["values"][0]

        if data == 'creat':

            await self.new_callback(interation)

        elif data == 'pass':

            await interation.response.edit_message()

        else:

            self.User.ChooseChar(int(data))

            Character = self.User.SelectedCharacter

            await self.screen.Show(Character.ScreenName)

            await interation.response.edit_message (embed = self.screen.Embed, view = self.screen)
               
    async def new_callback(self, interation: Interaction):

        self.User.AppendCharacter()

        await self.screen.Show('reg_stage1')

        await interation.response.edit_message (embed = self.screen.Embed, view = self.screen)
