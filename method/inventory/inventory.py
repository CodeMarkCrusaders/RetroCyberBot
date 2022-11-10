from cProfile import label
import sys
import os

from Data_classes.character import Character
from .options import scroll
from Data_classes.stat import Damag, Inventory , Medication
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction
import discord
from method.Base import Base 
from Thing.Thing import all_item_to_creat, all_item
from .Scrn import GetArmor, GetWeapon, GetItemData
#from screen import Screen

class inventory(Base):

    def __init__(self, screen):
        super().__init__(screen)
        self.Data = self.Screen.Data
        if 'n' not  in self.Data.keys():
            self.Data['n'] = 0 

        self.Screen.Embed = Embed(
            title = 'Инвентарь',
            colour = discord.Color.dark_green()
        )

        self.Screen.Embed.add_field(
            name = f'--------ТЕЛО--------',
            value = GetArmor(self.Character)
        )

        self.Screen.Embed.add_field(
            name = f'--------ОРУЖИЕ--------',
            value = GetWeapon(self.Character)
        )

        scroll_Select = Select(
            options = scroll(self.Character.Inventory, self.Data['n'], self.Data.get('id')),
            row = 0
        )
        scroll_Select.callback = self.Select
        self.Screen.add_item(scroll_Select)

    
    async def Select(self, interation: Interaction):

        if interation.data['values'][0][0] == '@':

            self.Data['n'] = int(interation.data['values'][0][0].split('@')[1])

            await self.Update(interation)

        else:

            self.Data['id'] = int(interation.data['values'][0])

            interation.data['values'][0] = 'detail'

            await self.Transition(interation)

class detail(inventory):

    def __init__(self, screen):
        super().__init__(screen)
        self.item = self.Character.Inventory.GetItem(self.Data['id'])
        
        self.Screen.Embed = Embed(
            title = f'{self.item.general.name}',
            colour = discord.Color.dark_green()
        )

        self.Screen.Embed.add_field(
            name = f'--------Описание--------',
            value = self.item.general.desp
        )

        self.Screen.Embed.add_field(
            name = f'--------Параметры--------',
            value = GetItemData(self.item)
        )
        
        if self.item.cloth != None:
            Dress_Button = Button(
                label = 'Снять'if self.Character.VitalStat.Dress_don(self.item) else "Надеть",
                style = ButtonStyle.grey,
                row = 1 
            )
            Dress_Button.callback = self.Dress
            self.Screen.add_item(Dress_Button)

        if self.item.do != None:
            Do_Button = Button(
                label = "Применить",
                style = ButtonStyle.grey,
                row = 1 
            )
            Do_Button.callback = self.Do
            self.Screen.add_item(Do_Button)

        Throw_out_Button = Button(
            label = "Выбросить" ,
            style = ButtonStyle.grey,
            row = 1 
        )
        Throw_out_Button.callback = self.Throw_out
        self.Screen.add_item(Throw_out_Button)

        Pick_up_Button = Button(
            label = 'Убрать'if self.Character.ActionStat.EquipedWeapon == self.item else "Взять" ,
            style = ButtonStyle.grey,
            row = 1 
        )
        Pick_up_Button.callback = self.Pick_up
        self.Screen.add_item(Pick_up_Button)

    async def Select(self, interation: Interaction):

        if interation.data['values'][0][0] == '@':

            pass

        elif int(interation.data['values'][0]) == self.Data['id']:

            self.Data['id'] = None

            interation.data['values'][0] = 'inventory'

            await self.Transition(interation)

        else:

            self.Data['id'] = int(interation.data['values'][0])

            interation.data['values'][0] = 'detail'

            await self.Update(interation)

    async def Dress(self, interation: Interaction):

        await self.Character.Dress(self.item)

        await self.Update(interation)

    async def Do (self, interation: Interaction):

        await self.Character.Do(self.item)

        await self.Update(interation)

    async def Pick_up(self, interation: Interaction):

        await self.Character.Pick_up(self.item)

        await self.Update(interation)
    
    async def Throw_out(self, interation: Interaction):

        await self.Character.Inventory.Throw_out(self.item.general.id)

        interation.data["custom_id"]= 'inventory'

        await self.Transition(interation)

