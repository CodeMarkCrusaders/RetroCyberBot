import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction
import discord
from Data_classes.memcell import MemoryCell
from method.reg_stage3.options import list_traits
from method.Base import Base 
#from screen import Screen

class reg_stage3(Base):

    def __init__(self, screen):
        super().__init__(screen)

        self.Data = self.Character.RegStage3
        self.User.SetValue = self.Data.SetMeaning
        self.Screen.Embed = Embed(
            title = 'Создание персонажа этап III. \nКакие у вас отличительные особености?',
            colour = discord.Color.dark_green()
        )
        self.Screen.ScreenName = 'reg_stage3'
        self.Character.ScreenName = 'reg_stage3'
        list_trait_1, list_trait_2 = list_traits(self.Data.GetAllMemory())

        Trait_Select_1 = Select(
            options = list_trait_1,
            row = 1
        )
        Trait_Select_1.callback = self.СhooseSetMeaning
        self.Screen.add_item(Trait_Select_1)

        Trait_Select_2 = Select(
            options = list_trait_2,
            row = 2
        )
        Trait_Select_2.callback = self.СhooseSetMeaning
        self.Screen.add_item(Trait_Select_2)

        Back_Button = Button(
            label = "Назад",
            style = ButtonStyle.grey,
            custom_id = 'reg_stage2',
            row = 4 
        )
        Back_Button.callback = self.Transition
        self.Screen.add_item(Back_Button)

        Menu_Button = Button(
            label = "В меню",
            style = ButtonStyle.grey,
            custom_id = 'menu',
            row = 4 
        )
        Menu_Button.callback = self.Transition
        self.Screen.add_item(Menu_Button)

        End_Button = Button(
            label = 'Закончить',
            style = ButtonStyle.green,
            custom_id = 'inventory',
            row = 4
        )
        End_Button.callback = self.EndCallback
        self.Screen.add_item(End_Button)

        
    async def EndCallback(self, interation: Interaction):
        await self.Character.RegEnd()

        await self.Transition(interation)




        