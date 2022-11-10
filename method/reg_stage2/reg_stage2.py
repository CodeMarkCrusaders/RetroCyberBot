import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction
from Data_classes.memcell import MemoryCell
from method.Base import Base 
from method.reg_stage2.NumberButton import NumberButtonCreate
from method.reg_stage2.Goat import Question
#from screen import Screen

class reg_stage2(Base):

    def __init__(self, screen):
        super().__init__(screen)

        self.Data = self.Character.RegStage2
        self.User.SetValue = self.Data.SetMeaning
        self.QuestionNumber = self.Data.GetMemory('question_number')
        self.Screen.Embed = Question[self.QuestionNumber]
        self.Screen.ScreenName = 'reg_stage2'
        self.Character.ScreenName = 'reg_stage2'
        self.Data.СhooseMeaning('room_' + str(self.QuestionNumber))

        

        NumberButtonList = NumberButtonCreate(self.Data.GetMemory('room_' + str(self.QuestionNumber)))
        for button in NumberButtonList:
            button.callback = self.SetMeaning
            self.Screen.add_item(button)

        Previous_Button = Button(
            label = '◄',
            style = ButtonStyle.gray if not self.QuestionNumber == 0 else ButtonStyle.red,
            disabled = self.QuestionNumber == 0,
            custom_id = '!' + str(int(self.QuestionNumber) - 1),
            row = 3
        )
        Previous_Button.callback = self.Leaf_callback
        self.Screen.add_item(Previous_Button)

        Position_Button = Button(
            label = self.QuestionNumber + 1,
            style = ButtonStyle.grey,
            custom_id = 'question_number',
            disabled = True,
            row = 3
        )
        Position_Button.callback = self.СhooseMeaning
        self.Screen.add_item(Position_Button)

        Next_Button = Button(
            label = '►',
            style = ButtonStyle.gray if not self.QuestionNumber == 9 else ButtonStyle.red,
            disabled = self.QuestionNumber == 9,
            custom_id = '!' + str(int(self.QuestionNumber) + 1),
            row = 3
        )
        Next_Button.callback = self.Leaf_callback
        self.Screen.add_item(Next_Button)

        Back_Button = Button(
            label = "Назад",
            style = ButtonStyle.grey,
            custom_id = 'reg_stage1',
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

        Further_Button = Button(
            label = 'Далее',
            style = ButtonStyle.green if self.Data.Filled() else ButtonStyle.red,
            disabled = not self.Data.Filled(),
            custom_id = 'reg_stage3',
            row = 4
        )
        Further_Button.callback = self.Transition
        self.Screen.add_item(Further_Button)

    async def Leaf_callback(self, interation: Interaction):

        self.Data.СhooseMeaning('question_number')

        self.Data.SetMeaning(interation.data['custom_id'][1::])

        await self.Update(interation)