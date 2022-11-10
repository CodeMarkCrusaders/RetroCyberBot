from copy import copy
from .memcell import MemoryCell
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from .stat import ActionStat, Damag, Medication, Special,StartSpecial, Ability,StartAbility, General, LVL, StartVitalStat, VitalStat, Mod, Triger, Inventory
from Thing.Thing import  Thing, all_clothing_to_creat, Buff

class Character():

    def __init__(self, ID) -> None:

        self.RegStage1 = MemoryCell(
                {
                    'name': {
                        'CM': str,
                        'EM': None,
                        'SV': None
                    },
                    'gender': {
                        'CM': str,
                        'EM': None,
                        'SV': None
                    },
                    'race': {
                        'CM': str,
                        'EM': None,
                        'SV': None
                    },
                }
                
            )
        self.RegStage2 = MemoryCell(
                {
                    'question_number': {
                        'CM': int,
                        'EM': None,
                        'SV': 0
                    },
                    'room_0': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_1': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_2': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_3': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_4': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_5': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_6': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_7': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_8': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                    'room_9': {
                        'CM': int,
                        'EM': None,
                        'SV': None
                    },
                }
            )
        self.RegStage3 = MemoryCell(
                {
                    'trait_1': {
                        'CM': str,
                        'EM': None,
                        'SV': 'None'
                    },
                    'trait_2': {
                        'CM': str,
                        'EM': None,
                        'SV': 'None'
                    },
                }
            )        

        self.Data = None
        self.Hit : Damag = None
        self.Target : Character = None

        self.__ID = ID
        self.ScreenName = None

        self.Special    : Special= None
        self.Ability    : Ability= None
        self.General    : General = None
        self.lvl        : LVL = LVL()
        self.VitalStat  : VitalStat = None
        self.ActionStat : ActionStat = None
        self.Inventory : Inventory = Inventory()

        self.Buff : dict[str:Buff] = {}

    def GetID(self) -> int:

        return self.__ID

    def GetSaveData(self) -> dict:

        Data = {}

        Data.update(self.RegStage1.GetAllMemory())
        Data.update(self.RegStage2.GetAllMemory())
        Data.update(self.RegStage3.GetAllMemory())

        Data['screen_name'] = self.ScreenName

        return Data

    def GetBasicData(self) -> dict:

        if self.General == None:

            Data = self.RegStage1.GetAllMemory()

        else:

            Data = self.General.__dict__

        Data['lvl'] = self.lvl.lvl

        return Data

    def Load(self, Data: dict):

        self.ScreenName = Data['screen_name']

        if self.General == None:
            self.RegStage1 = MemoryCell(
            {
                'name': {
                    'CM': str,
                    'EM': None,
                    'SV': Data['name']
                },
                'gender': {
                    'CM': str,
                    'EM': None,
                    'SV': Data['gender']
                },
                'race': {
                    'CM': str,
                    'EM': None,
                    'SV': Data['race']
                },
            }
        )
            self.RegStage2 = MemoryCell(
            {
                'question_number': {
                    'CM': int,
                    'EM': None,
                    'SV': 0
                },
                'room_0': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_0']
                },
                'room_1': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_1']
                },
                'room_2': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_2']
                },
                'room_3': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_3']
                },
                'room_4': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_4']
                },
                'room_5': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_5']
                },
                'room_6': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_6']
                },
                'room_7': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_7']
                },
                'room_8': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_8']
                },
                'room_9': {
                    'CM': int,
                    'EM': None,
                    'SV': Data['room_9']
                },
            }
        )
            self.RegStage3 = MemoryCell(
                {
                    'trait_1': {
                        'CM': str,
                        'EM': None,
                        'SV': Data['trait_1']
                    },
                    'trait_2': {
                        'CM': str,
                        'EM': None,
                        'SV': Data['trait_2']
                    },
                }
            )

        else: 

            pass

    async def RegEnd(self):

        from buff_list.buff import all_buff

        answerlist = [value for value in self.RegStage2.GetAllMemory().values()][1:11]
        self.General = General(self.RegStage1.GetMemory('name') , self.RegStage1.GetMemory('race') ,self.RegStage1.GetMemory('gender'))

        self.Ability = StartAbility(answerlist, self.General.race)

        self.Special = StartSpecial(answerlist)
        

        #self.ListModifier = ListModified(self)

        #if self.General.race in ['unicorn','changeling']:
#
        #    await self.AddAptitude(all_aptitude['horn'])
#
#
        #if self.General.race in ['pegasus','changeling','griffin']:
#
        #    await self.AddAptitude(all_aptitude['wings'])

        self.VitalStat = StartVitalStat(self.Special, self.General.race)

        self.ActionStat = ActionStat(self.Special)

        for apt in self.RegStage3.GetAllMemory().values():

            await self.AddBuff(all_buff[apt])


        for AbilName in self.Ability.__dict__.keys():

            if self.Ability.__dict__[AbilName] == None:

                continue

            if AbilName in ['science','medicine','repair','magic']:
                self.Ability.__dict__[AbilName].org_val += self.Special.I.val * 3 + self.Special.L.val + 5 

            elif AbilName in ['barter','speech'] :
                self.Ability.__dict__[AbilName].org_val += self.Special.C.val * 3 + self.Special.L.val + 5 

            elif AbilName in ['lockpick','energy_weapons','explosives',' throwing']:
                self.Ability.__dict__[AbilName].org_val += self.Special.P.val * 3 + self.Special.L.val + 5 

            elif AbilName == 'melee_weapons':
                self.Ability.__dict__[AbilName].org_val += self.Special.S.val * 3 + self.Special.L.val + 5 

            elif AbilName in ['big_guns','unarmed']:
                self.Ability.__dict__[AbilName].org_val += self.Special.E.val * 3 + self.Special.L.val + 5 

            elif AbilName in ['small_guns','sneak','fly']:
                self.Ability.__dict__[AbilName].org_val += self.Special.A.val * 3 + self.Special.L.val + 5 

        self.Ability.Update()
        await self.BuffUpdate()

        print(1)
        from Thing.Thing import all_item
        self.Inventory.Append(all_item.catalog[0],all_item.catalog[1],all_item.catalog[2])

    async def BuffUpdate(self):

        #if 'all' in field:

        #    field += ['special','ability','actionstat','vitalstat']

        await self.Reset(('Special','Ability','ActionStat','lvl', "VitalStat"))

        for_pop = []
        for_prime : dict = copy(self.Buff)
        len_before = 0
        
        while len_before != len(for_prime):
            len_before = len(for_prime)
            for_pop_n = []
            for buff in for_prime.values():
                if await self.TrigerHandler(buff.triger):

                    for_pop_n.append(buff.id)

                    if buff.mod != None:
                        await self.ModHandler(buff.mod)
                    if buff.heal != None:
                        await self.SetMed(buff.dmg)
                    if buff.dmg != None:
                        await self.SetDmg(buff.heal)
                
                if buff.mod == None:
                    for_pop.append(buff.id)
            
                elif buff.heal != None:
                    buff.heal = None

                elif buff.dmg != None:
                    buff.dmg = None

            for id in for_pop_n:
                for_prime.pop(id)

        for id in for_pop:
            self.Buff.pop(id)

        self.Special.Update()
        self.Ability.Update()
        self.VitalStat.Update()

    async def Dress(self, clothing: Thing = None, id = None):

        if id != None:
            clothing = self.Inventory.GetItem(id)

        if self.ActionStat.EquipedWeapon == clothing:

            self.ActionStat.EquipedWeapon = None

        if clothing is self.VitalStat.__dict__[clothing.cloth.limb[0]].EquippedArmor:

            for buff in self.VitalStat.__dict__[clothing.cloth.limb[0]].EquippedArmor.cloth.buff:

                self.Buff.pop(buff.id)

            for limb in clothing.cloth.limb:

                self.VitalStat.__dict__[limb].Equipped(all_clothing_to_creat['heading_'+limb])
            
            await self.BuffUpdate()

            return 

        if  not await self.TrigerHandler(clothing.cloth.don_con):

            return

        for limb in clothing.cloth.limb:

            for buff in self.VitalStat.__dict__[limb].EquippedArmor.cloth.buff:

                self.Buff.pop(buff.id)

            for limb in self.VitalStat.__dict__[limb].EquippedArmor.cloth.limb:

                self.VitalStat.__dict__[limb].Equipped(all_clothing_to_creat['heading_'+limb])

            self.VitalStat.__dict__[limb].Equipped(clothing)
        
        await self.AddBuff(clothing.cloth.buff)

    async def Pick_up(self, object: Thing = None, id = None):

        if id != None:
            object = self.Inventory.GetItem(id)

        if self.VitalStat.Dress_don(object):

            await self.Dress(object)

        if object is self.ActionStat.EquipedWeapon:

            for buff in self.ActionStat.EquipedWeapon.weapon.buff:

                self.Buff.pop(buff.id)

            self.ActionStat.Pick_up(None)
            
        if not await self.TrigerHandler(object.weapon.don_con):

            return

        self.ActionStat.Pick_up(object)

        await self.AddBuff(object.weapon.buff)

        await self.BuffUpdate()

    async def ModHandler(self, array_mod: tuple[Mod]):

        for mod in array_mod:

                await self.__dict__[mod.field[0]].ModHandler(mod)

    async def BuffHadler(self, buff: Buff):

        if await self.TrigerHandler(buff.triger):
            if buff.mod != None:
                await self.ModHandler(buff.mod)
            elif buff.heal != None:
                for heal in buff.heal:
                    await self.SetMed(heal)
            elif buff.dmg != None:
                for dmg in buff.dmg:
                    await self.SetDmg(dmg)

    async def TrigerHandler(self, triger_list : dict[str:Triger]) -> bool:
        
        if triger_list == None:
            return True

        answer_or = len(triger_list['OR']) == 0
        answer_and = True
        answer_not = True

        for triger in triger_list['OR']:

            answer_or = answer_or or self.__dict__[triger.field[0]].TrigerHandler(triger) if  self.__dict__[triger.field[0]] != None else False

        for triger in triger_list['AND']:

            answer_and = answer_and and self.__dict__[triger.field[0]].TrigerHandler(triger) if  self.__dict__[triger.field[0]] != None else False
        
        for triger in triger_list['NOT']:

            answer_not = answer_not and not self.__dict__[triger.field[0]].TrigerHandler(triger) if  self.__dict__[triger.field[0]] != None else False

        return answer_or and answer_and and answer_not
    
    async def AddBuff(self, list_buff: tuple[Buff]):

        for buff in list_buff:

            buff:Buff

            self.Buff[buff.id] = buff

        await self.BuffUpdate()
    
    async def Reset(self, array_of_reset : list[str]):

        for part in array_of_reset:

            self.__dict__[part].Reset()

    async def DelBuff(self, id : str):

        self.Buff.pop(id)

        self.BuffUpdate()

    async def SetMed(self, Med: list[Medication]):

        Med_list = list(Med)

        for med in Med_list:

            await self.VitalStat.GetMed(med)

            await self.BuffUpdate()

    async def SetDmg(self, Dmg: tuple[Damag]):
        
        Dmg_list = list(Dmg)

        for dmg in Dmg_list:

            self.Hit = dmg

            await self.AddBuff(dmg.buff_before)

            await self.VitalStat.GetDmg(dmg)

            self.Hit = None

            await self.AddBuff(dmg.buff_after)

        for dmg in Dmg_list:

            for limb in dmg.Limb:

                if self.VitalStat.__dict__[limb].EquippedArmor.general.fracture == -1:

                    await self.Fracture(self.VitalStat.__dict__[limb].EquippedArmor)

        return [buff for buff in self.Buff.values() if buff.id.split('!')[0] == 'answer' ]

    async def Do(self, object):

        await self.SetDmg(object.do.dmg)

        await self.SetMed(object.do.heal)

        await self.AddBuff(object.do.buff)

    async def GetDmg(self, attack_type, target):

        await self.BuffUpdate()

        Dmg = self.ActionStat.GetDmg(attack_type, target, self.General.race, self.Special.S.val)

        self.Target = None

        await self.BuffUpdate()

        return Dmg

    async def GetAttack(self, attack_type, target, distance = None , ability = None, chance = None):

        await self.BuffUpdate()

        weapon = self.ActionStat.EquipedWeapon
        if chance == None:
            if attack_type == 'melee':
                chance = max(self.Special.L.val, (self.Ability.__dict__[ability if ability != None else weapon.weapon.melee.ability[0]].val - self.Target.Ability.__dict__[ability if ability != None else weapon.weapon.melee.ability[0]].val / 2) * (weapon.weapon.melee.AttackFactor + self.ActionStat.AttackData.AttackFactor))

            else:
                data = weapon.weapon.__dict__[attack_type]
                chance = max(self.Special.L.val, self.Ability.__dict__[ability if ability != None else data.ability[0]].val * data.distance.__dict__[distance] * (data.AttackFactor + self.ActionStat.AttackData.AttackFactor))


        Dmg = self.ActionStat.Attack(attack_type, target, self.General.race, self.Special.S.val, chance)
        if attack_type == 'quit':
            self.ActionStat.EquipedWeapon = None

        elif self.ActionStat.EquipedWeapon.general.fracture == -1:
            await self.Fracture(self.ActionStat.EquipedWeapon)

        self.Target = None

        await self.BuffUpdate()

        return Dmg    

    async def Fracture(self,thing):

        if self.ActionStat.EquipedWeapon is thing:
            self.ActionStat.EquipedWeapon = None

        if self.VitalStat.Dress_don(thing):
            await self.Dress(thing)

        if thing in self.Inventory.catalog:
            self.Inventory.Del(thing)

    async def Throw_out(self,thing):

        if self.ActionStat.EquipedWeapon is thing:
            self.ActionStat.EquipedWeapon = None

        if self.VitalStat.Dress_don(thing):
            await self.Dress(thing)

        if thing in self.Inventory.catalog:
            self.Inventory.Throw_out(thing)