import sys
import os
import discord
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction
#from screen import Screen
from Data_classes.memcell import MemoryCell
from method.reg_stage1.options import list_gender, list_race 
from method.Base import Base 

class reg_stage1(Base):
    def __init__(self ,screen):
        super().__init__(screen)
        self.Data = self.Character.RegStage1
        self.User.SetValue = self.Data.SetMeaning

        self.Screen.Embed = Embed(
            title = 'Создание персонажа этап I',
            colour = discord.Color.dark_green()
            )
        self.Screen.ScreenName = 'reg_stage1'

        Back_Button = Button(
            label = "Назад",
            style = ButtonStyle.grey,
            disabled = not self.Screen.BackPos(),
            custom_id = 'back',
            row = 4 
        )
        Back_Button.callback = self.Transition
        self.Screen.add_item(Back_Button)

        BasicInf = self.Data.GetAllMemory()

        Name_Button = Button(
            label = "Имя" if BasicInf['name'] == None else BasicInf['name'],
            style = ButtonStyle.grey if BasicInf['name'] == None else ButtonStyle.green,
            custom_id = 'name',
            row = 0
        )
        Name_Button.callback = self.СhooseMeaning
        self.Screen.add_item(Name_Button)

        Race_Select = Select(
            placeholder = 'Выберте расу персонажа',
            options = list_race(BasicInf['race']),
            row = 1
        )
        Race_Select.callback = self.СhooseSetMeaning
        self.Screen.add_item(Race_Select)

        Race_Select = Select(
            placeholder = 'Выберте пол персонажа',
            options = list_gender(BasicInf['gender']),
            row = 2
        )
        Race_Select.callback = self.СhooseSetMeaning
        self.Screen.add_item(Race_Select)

        Further_Button = Button(
            label = 'Далее',
            style = ButtonStyle.green if self.Data.Filled() else ButtonStyle.red,
            disabled = not self.Data.Filled(),
            custom_id = 'reg_stage2',
            row = 4
        )
        Further_Button.callback = self.Transition
        self.Screen.add_item(Further_Button)



        

