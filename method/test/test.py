import sys
import os

from Data_classes.character import Character
from method.test.options import special_list, ability_list , Vital_list
from Data_classes.stat import Damag , Medication
sys.path.append(os.path.dirname(sys.path[0]))
from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction
import discord
from method.Base import Base 
from Thing.Thing import all_item_to_creat, all_item
from random import randint
#from screen import Screen

class test(Base):

    def __init__(self, screen):
        super().__init__(screen)
        self.SData = self.Character.Special
        self.AData = self.Character.Ability
        self.VData = self.Character.VitalStat
        self.selected = self.Character.Data
        self.Screen.Embed = Embed(
            title = 'Тест',
            colour = discord.Color.dark_green()
        )
        self.Screen.Embed.add_field(
            name = f'--------SPECIAL--------',
            value = self.SData.GetData()
        )
        self.Screen.Embed.add_field(
            name = '--------Ability--------',
            value = self.AData.GetData()
        )
        self.Screen.Embed.add_field(
            name = f'--------Vital--------',
            value = self.VData.GetData()
        )
        self.Screen.Embed.add_field(
            name = f'Armor',
            value = (   "Head " + f"{self.VData.Head.Armor.F} - {self.VData.Head.Armor.M} {self.VData.Head.EquippedArmor.general.strength}\n\n"+
                        "Body " + f"{self.VData.Body.Armor.F} - {self.VData.Body.Armor.M} {self.VData.Body.EquippedArmor.general.strength}\n\n"+
                        "FLL " + f"{self.VData.FLL.Armor.F} - {self.VData.FLL.Armor.M} {self.VData.FLL.EquippedArmor.general.strength}\n\n"+
                        "FRL " + f"{self.VData.FRL.Armor.F} - {self.VData.FRL.Armor.M} {self.VData.FRL.EquippedArmor.general.strength}\n\n"+
                        "BLL " + f"{self.VData.BLL.Armor.F} - {self.VData.BLL.Armor.M} {self.VData.BLL.EquippedArmor.general.strength}\n\n"+
                        "BRL " + f"{self.VData.BRL.Armor.F} - {self.VData.BRL.Armor.M} {self.VData.BRL.EquippedArmor.general.strength}\n\n"+
                        "Horn " + f"{self.VData.Horn.Armor.F} - {self.VData.Horn.Armor.M} {self.VData.Horn.EquippedArmor.general.strength}\n\n")
        )
        self.Screen.ScreenName = 'test'
        self.Character.ScreenName = 'test'


        Special_Select = Select(
            options = special_list(self.selected),
            row = 0
        )
        Special_Select.callback = self.Select
        self.Screen.add_item(Special_Select)

        Ability_Select = Select(
            options = ability_list(self.selected),
            row = 1
        )
        Ability_Select.callback = self.Select
        self.Screen.add_item(Ability_Select)

        Vital_Select = Select(
            options = Vital_list(self.selected),
            row = 2
        )
        Vital_Select.callback = self.Select
        self.Screen.add_item(Vital_Select)

        attack_button = Button(
            label = 'Атака',
            custom_id = '734101135748497419!0',
            row = 3
        )
        attack_button.callback = self.attack
        self.Screen.add_item(attack_button)

        down_Button = Button(
            label = "⬇",
            style = ButtonStyle.grey,
            row = 4 
        )
        down_Button.callback = self.down
        self.Screen.add_item(down_Button)

        up_Button = Button(
            label = "⬆️",
            style = ButtonStyle.grey,
            row = 4 
        )
        up_Button.callback = self.Up
        self.Screen.add_item(up_Button)

        dmg_Button = Button(
            label = "DMG",
            style = ButtonStyle.grey,
            row = 4 
        )
        dmg_Button.callback = self.DMG
        self.Screen.add_item(dmg_Button)

        med_Button = Button(
            label = "Med",
            style = ButtonStyle.grey,
            row = 4 
        )
        med_Button.callback = self.MED
        self.Screen.add_item(med_Button)

        dress_Button = Button(
            label = "dress",
            style = ButtonStyle.grey,
            row = 4 
        )
        dress_Button.callback = self.Dress
        self.Screen.add_item(dress_Button)
        
    async def Select(self, interation: Interaction):
        
        self.Character.Data = interation.data['values'][0]

        await self.Update(interation)

    async def Up(self, interation: Interaction):
        
        if self.selected != None:

            if self.selected in ['S','P','E','C','I','A','L']:
                self.SData.__dict__[self.selected].ChangeFactorEd(1)
            
            else:
                
                self.AData.__dict__[self.selected].ChangeFactorEd(1)

        await self.Update(interation)

    async def down(self, interation: Interaction):

        if self.selected != None:

            if self.selected in ['S','P','E','C','I','A','L']:
                self.SData.__dict__[self.selected].ChangeFactorEd(-1)

            else:

                self.AData.__dict__[self.selected].ChangeFactorEd(-1)

        await self.Update(interation)

    async def DMG(self, interation: Interaction):

        dmg = Damag( (self.selected,), 11,'F', False, Weapon = ("as",))

        await self.Character.SetDmg(dmg)

        await self.Update(interation)

    async def MED(self, interation: Interaction):

        hl = all_item_to_creat['healing_potion']

        await self.Character.Do(hl)

        await self.Update(interation)

    async def Dress(self, interation: Interaction):

        await self.Character.Dress(all_item_to_creat['black_glasses'])

        await self.Update(interation)
        
    async def attack(self, interation: Interaction):

        from Data_classes.all_user import AllUser

        if self.Character.ActionStat.EquipedWeapon == None:
            await self.Character.Pick_up(all_item.catalog[0])

        target : Character = AllUser.all_character[interation.custom_id]

        self.Character.Target = target

        Dmg = await self.Character.GetAttack('range',['Head'],"close", chance = 100)

        for dmg in Dmg:

            if randint(1,100) <= dmg.Chance:

                await self.Character.AddBuff(await target.SetDmg(Dmg))

        await self.Update(interation)
