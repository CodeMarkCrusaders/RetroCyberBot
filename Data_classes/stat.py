from dataclasses import dataclass
from random import randint
import sys
import os
from types import NoneType

sys.path.append(os.path.dirname(sys.path[0]))



######################################
@dataclass 
class Triger:
    field : tuple[str]
    con : str
    n : str

@dataclass
class Mod:
    field : tuple[str]
    ed : bool
    n : str

class _parameter:
    def __init__(self, st) -> None:
        self.__stage = st

    async def ModHandler(self, mod: Mod):

        if self.__stage == len(mod.field) - 1:

            if mod.ed:
                if isinstance(mod.field[-1], tuple):
                    for fl in mod.field[-1]:
                        self.__dict__[fl] = self.__dict__[fl] + float(mod.n)
                else:
                    self.__dict__[mod.field[-1]] = self.__dict__[mod.field[-1]] + float(mod.n)
            else:
                self.__dict__[mod.field[-1]] = self.__dict__[mod.field[-1]] * float(mod.n)

        else:
            if self.__dict__[mod.field[self.__stage]] == None:
                return
            await self.__dict__[mod.field[self.__stage]].ModHandler(mod)

    def TrigerHandler(self, triger: Triger):
        if triger.con == 'rnd':
            return bool(randint(0,1)) if triger.n == None else randint(0,100) <= int(triger.n)

        if self.__stage == len(triger.field) - 1:

            if triger.con == '<':
                return self.__dict__[triger.field[-1]] <= float(triger.n)

            elif triger.con == '>':
                return self.__dict__[triger.field[-1]] >= float(triger.n)

            elif triger.con == '==':
                return self.__dict__[triger.field[-1]] == triger.n

            elif triger.con == 'in':
                return triger.n in self.__dict__[triger.field[-1]]

            elif triger.con == 'fracture':
                return self.__dict__[triger.field[-1]] == -1

        else:
            return self.__dict__[triger.field[self.__stage]].TrigerHandler(triger)
            
    def Reset(self):

        for name in self.__dict__.keys():
            if not isinstance(self.__dict__[name], Value):
                continue
            self.__dict__[name].FactorEd = 0
            self.__dict__[name].FactorAm = 1

class Damag(_parameter):

    def __init__(self, Limb: tuple[str], Dmg: float, Type: str, Ignore: bool = False, Crit: float = None, Weapon  : tuple[str] = None, Forward : tuple[str] = None, BulletType: tuple[str] = None, buff_before = tuple(), buff_after = tuple(), Chance : float = 0) -> None:
        super().__init__(1)
        self.Limb = Limb      
        self.Dmg = Dmg       
        self.Type = Type      
        self.Ignore = Ignore    
        self.Crit = Crit
        self.Chance = Chance
        
        self.Weapon = Weapon    
        self.Forward = Forward   
        self.BulletType = BulletType

        self.buff_before = buff_before
        self.buff_after = buff_after

@dataclass
class Medication:

    Limb        : tuple[str]
    RegenED     : float
    RegenAmMax  : float
    RegenAmHere : float

@dataclass
class Buff:

    id : str
    name : str
    desp : str
    triger: dict[str:Triger] | NoneType
    mod: tuple[Mod]
    heal : tuple[Medication]
    dmg: tuple[Damag]

######################################

def Do(plan:dict):
    if plan == None:
        return None
    return do(
        buff = tuple([]),
        heal = tuple([Medication(Limb = tuple(heal['limb']) , RegenED = float(heal.get('regen_ed', 0)), RegenAmHere = float(heal.get('regen_am_here', 0)), RegenAmMax = float(heal.get('regen_am_max', 0))) for heal in plan.get('heal',[] )]),
        dmg = tuple([Damag(Limb = tuple(dmg['limb']), Dmg = float(dmg['dmg']), Type = dmg.get('type', 'F'), Crit = float(dmg['crit']) if dmg.get('crit') != None else None, Ignore = dmg.get('ignore') if dmg.get('ignore', 0) == True else float(dmg.get('ignore'))) for dmg in plan.get('dmg', [])]),
    )

class Clothing(_parameter):

    def __init__(self,F: int,M: int,limb: tuple[str],don_con: dict[str:Triger] | NoneType,buff: tuple[Buff]) -> None:
        super().__init__(4)
        self.F = F         
        self.M = M      
        self.limb = limb      
        self.don_con = don_con      
        self.buff = buff      

class do:
    def __init__(self, buff:tuple[Buff], heal: tuple[Medication], dmg: tuple[Damag]) -> None:
        self.buff = buff
        self.heal = heal
        self.dmg = dmg

class general(_parameter):
    def __init__(self, plan: dict) -> None:

        super().__init__(4)

        self.id : str = plan['id']
        self.name : str = plan['name']
        self.desp : str = plan['desp']
        self.cost : int = plan['cost']
        self.strength : list[float] = list(map(float,plan['strength'])) if plan.get('strength') != None else None
        self.weight : float = float(plan['weight'])
        self.type : tuple[str] = plan['type']
        self.fracture : int = plan['fracture']
        self.magazine : list[float] = list(map(float,plan.get('magazin'))) if plan.get('magazin') != None else None

############################################

class Value:

    def __init__(self, start_number = 0, ed = 0 , am = 1) -> None:
        
        self.org_val     : int = start_number
        self.val         : int = 0
        self.FactorEd    : list[int] = ed
        self.FactorAm    : list[int] = am

        self.update()

    def update(self):

        self.val = int((self.org_val + self.FactorEd) * self.FactorAm)

    def ChangeFactorEd(self, val):

        self.FactorEd += val

        self.update()

    def ChangeFactorAm(self, val):

        self.FactorAm += val

        self.update()

    def __str__(self) -> str:
        
        return str(self.val)

    def __add__(self, other):
        
        return Value(start_number = self.org_val, ed = self.FactorEd + other, am = self.FactorAm)

    def __sub__(self, other):

        return Value(start_number = self.org_val, ed = self.FactorEd - other, am = self.FactorAm)

    def __mul__(self, other):
        
        return Value(start_number = self.org_val, ed = self.FactorEd, am = self.FactorAm + other - 1)

    def  __truediv__(self, other):
        
        return Value(start_number = self.org_val, ed = self.FactorEd, am = self.FactorAm - other + 1)

    def __le__(self, other):

        return self.val <= other

    def __ge__(self, other):

        return self.val >= other

    def __eq__(self, other):

        return self.val == other

class Special(_parameter):

    def __init__(self) -> None:
        super().__init__(1)
        
        self.S : Value = Value(1) 
        self.P : Value = Value(1)   
        self.E : Value = Value(1)   
        self.C : Value = Value(1)   
        self.I : Value = Value(1)   
        self.A : Value = Value(1)   
        self.L : Value = Value(1)

    def Update(self):

        self.S.update()
        self.P.update()
        self.E.update()
        self.C.update()
        self.I.update()
        self.A.update()
        self.L.update()

    def GetData(self) -> str:

        data = ''

        data += 'S - ' + str(self.S) + '\n'
        data += 'P - ' + str(self.P) + '\n'
        data += 'E - ' + str(self.E) + '\n'
        data += 'C - ' + str(self.C) + '\n'
        data += 'I - ' + str(self.I) + '\n'
        data += 'A - ' + str(self.A) + '\n'
        data += 'L - ' + str(self.L) + '\n'

        return data
        
class Ability(_parameter):

    def __init__(self) -> None:

        super().__init__(1)

        self.science          : Value = Value()         
        self.medicine         : Value = Value()     
        self.repair           : Value = Value() 
        self.barter           : Value = Value() 
        self.speech           : Value = Value() 
        self.lockpick         : Value = Value()     
        self.energy_weapons   : Value = Value()         
        self.explosives       : Value = Value()     
        self.quit             : Value = Value()     
        self.melee_weapons    : Value = Value()         
        self.big_guns         : Value = Value()     
        self.unarmed          : Value = Value() 
        self.small_guns       : Value = Value()     
        self.sneak            : Value = Value() 
        self.fly              = None
        self.magic            = None

    def Update(self):

        
        self.science.update()       
        self.medicine.update()      
        self.repair.update()        
        self.barter.update()        
        self.speech.update()        
        self.lockpick.update()      
        self.energy_weapons.update()
        self.explosives.update()    
        self.quit.update()      
        self.melee_weapons.update() 
        self.big_guns.update()      
        self.unarmed.update()       
        self.small_guns.update()    
        self.sneak.update() 
        if self.fly != None:        
            self.fly.update()  
        if self.magic != None:             
            self.magic.update()         

    def GetData(self) -> str:

        data = ''

        data += 'science' +     " - " + str (self.science  ) + '\n'   
        data += 'medicine' +    " - " + str (self.medicine ) + '\n'   
        data += 'repair' +      " - " + str (self.repair   ) + '\n'   
        data += 'barter' +      " - " + str (self.barter   ) + '\n'   
        data += 'speech' +      " - " + str (self.speech   ) + '\n'   
        data += 'lockpick' +    " - " + str (self.lockpick ) + '\n'   
        data += 'energy_weapons'" - " + str(self.energy_weapons) + '\n' 
        data += 'explosives' +  " - " + str(self.explosives    ) + '\n' 
        data += 'quit' +    " - " + str(self.quit     ) + '\n' 
        data += 'melee_weapons'+" - " + str(self.melee_weapons ) + '\n' 
        data += 'big_guns' +    " - " + str(self.big_guns      ) + '\n' 
        data += 'unarmed' +     " - " + str(self.unarmed       ) + '\n' 
        data += 'small_guns' +  " - " + str(self.small_guns    ) + '\n' 
        data += 'sneak' +       " - " + str(self.sneak         ) + '\n' 
        data += 'fly' +         " - " + str(self.fly           ) + '\n' 
        data += 'magic' +       " - " + str(self.magic         ) + '\n' 

        return data

def StartAbility(AnswerList, race):

    Data = Ability()

    if race in ['unicorn','changeling']:

        Data.magic = Value()

    if race in ['pegasus','changeling','griffin']:

        Data.fly = Value()

    for i in range( 10 ):

            if (i==0 and AnswerList[i]==2) or (i==1 and AnswerList[i]==2) or (i==2 and AnswerList[i]==1):
                Data.speech.org_val += 35

            elif (i==0 and AnswerList[i]==1) or (i==1 and AnswerList[i]==4):
                Data.science.org_val += 35

            elif (i==0 and AnswerList[i]==3) or (i==1 and AnswerList[i]==1):
                Data.melee_weapons.org_val += 35
                Data.quit.org_val += 15

            elif (i==0 and AnswerList[i]==4) or (i==2 and AnswerList[i]==3):
                Data.sneak.org_val += 35

            elif (i==1 and AnswerList[i]==3) or (i==6 and AnswerList[i]==2) or (i==7 and AnswerList[i]==4):
                Data.medicine.org_val += 35

            elif (i==2 and AnswerList[i]==2) or (i==3 and AnswerList[i]==4):
                Data.unarmed.org_val += 35
                Data.quit.org_val += 20

            elif (i==3 and AnswerList[i]==1) or (i==4 and AnswerList[i]==4) or (i==5 and AnswerList[i]==2):
                Data.explosives.org_val += 35
                if i==4 and AnswerList[i]==4:
                    Data.barter.org_val += 35

            elif (i==3 and AnswerList[i]==2) or (i==4 and AnswerList[i]==3):
                Data.big_guns.org_val += 35

            elif (i==4 and AnswerList[i]==2) or (i==6 and AnswerList[i]==3):
                Data.barter.org_val += 35

            elif (i==5 and AnswerList[i]==1) or (i==8 and AnswerList[i]==4):
                Data.lockpick.org_val += 35

            elif (i==5 and AnswerList[i]==3) or (i==6 and AnswerList[i]==4):
                Data.energy_weapons.org_val += 35

            elif (i==5 and AnswerList[i]==4) or (i==8 and AnswerList[i]==1):
                Data.repair.org_val += 35  

    Data.Update()

    return Data

def StartSpecial(AnswerList):


    Data = Special()
      
    for i in range( 10 ):
        if (i==0 and AnswerList[i]==2) or (i==1 and AnswerList[i]==2) or (i==2 and AnswerList[i]==1):
            Data.C.org_val += 2
            Data.P.org_val += 1 
        elif (i==0 and AnswerList[i]==1) or (i==1 and AnswerList[i]==4):
            Data.I.org_val += 2
            Data.P.org_val += 1
        elif (i==0 and AnswerList[i]==3) or (i==1 and AnswerList[i]==1):
            Data.S.org_val += 1
            Data.A.org_val += 1
            Data.E.org_val += 1
        elif (i==0 and AnswerList[i]==4) or (i==2 and AnswerList[i]==3):
            Data.A.org_val += 2
            Data.E.org_val += 1
        elif (i==1 and AnswerList[i]==3) or (i==6 and AnswerList[i]==2) or (i==7 and AnswerList[i]==4):
            Data.P.org_val += 1
            Data.I.org_val += 1
            Data.L.org_val += 1
        elif (i==2 and AnswerList[i]==2) or (i==3 and AnswerList[i]==4):
            Data.S.org_val += 2
            Data.E.org_val += 2
        elif (i==3 and AnswerList[i]==1) or (i==4 and AnswerList[i]==4) or (i==5 and AnswerList[i]==2):
            Data.S.org_val += 1
            Data.L.org_val += 2
            Data.I.org_val += 1
            if i==4 and AnswerList[i]==4:
                Data.C.org_val += 1
                Data.L.org_val += 1
        elif (i==3 and AnswerList[i]==2) or (i==4 and AnswerList[i]==3):
            Data.S.org_val += 1
            Data.E.org_val += 1
        elif (i==4 and AnswerList[i]==2) or (i==6 and AnswerList[i]==3):
            Data.C.org_val += 1
            Data.L.org_val += 1
        elif (i==5 and AnswerList[i]==1) or (i==8 and AnswerList[i]==4):
            Data.A.org_val += 1
            Data.P.org_val += 1
            Data.L.org_val += 1
        elif (i==5 and AnswerList[i]==3) or (i==6 and AnswerList[i]==4):
            Data.I.org_val += 1
            Data.S.org_val += 1
            Data.E.org_val += 1
        elif (i==5 and AnswerList[i]==4) or (i==8 and AnswerList[i]==1):
            Data.P.org_val += 2
            Data.I.org_val += 1

    Data.Update()

    return Data

@dataclass
class General(_parameter):
    
    name    :str
    race    :str
    gender  :str

@dataclass
class LVL(_parameter):

    def __init__(self) -> None:
        
        self.lvl : int = 1
        self.Exp : int = 0
        self.ExpFactor : int = 1
        self.exp_limit : list[int] = [300,900,2700,6500,14000,23000,48000,64000,85000,100000]

    def AddExp(self , exp):

        self.Exp += exp * self.ExpFactor

        if self.Exp >= self.exp_limit[self.lvl - 1]:

            self.lvl += 1

    def Reset(self):
        
        self.ExpFactor = 1

@dataclass
class Armor(_parameter):
    def __init__(self, F : Value = Value(1), M : Value = Value(1)) -> None:
        super().__init__(3)
        self.F = F
        self.M = M

@dataclass
class Resist(_parameter):
    def __init__(self, i) -> None:
        super().__init__(4)
        
        self.F = i
        self.M = i
        self.R = i
        self.E = i

class HP(_parameter):
    def __init__(self , Hp_Max) -> None:
        super().__init__(3)

        self.Hp_Max  : float = Hp_Max
        self.Hp      : float = Hp_Max
    
        self.MedFactorEd : int   = 0
        self.MedFactorAm : float = 1
    
        self.DmgFactorEd : Resist = Resist(0)
        self.DmgFactorAm : Resist = Resist(1)

    def GetDmg(self, dmg: float, type: str):

        self.Hp -= (dmg + self.DmgFactorEd.__dict__[type]) * self.DmgFactorAm.__dict__[type]
        self.Hp = max(0, self.Hp)

    def HpReset(self):

        self.Hp = self.Hp_Max

    def Reset(self):

        self.MedFactorAm = 1
        self.DmgFactorEd = 0

        self.DmgFactorAm = 1
        self.DmgFactorEd = 0

    def GetMed(self, regen):

        self.Hp += (regen + self.MedFactorEd) * self.MedFactorAm
        self.Hp = min(self.Hp_Max , self.Hp)

class Limb(_parameter):
    def __init__(self, hp):
        from Thing.Thing import Thing
        super().__init__(2)

        self.Health = HP(hp)
        self.Armor = Armor(Value(0),Value(0))

        self.EquippedArmor : Thing= None

        self.Injury_list = []

    def GetDmg(self, Dmg: Damag):
        dmg_st = Dmg.Dmg if Dmg.Crit == None else Dmg.Crit

        dmg = min(dmg_st,max(0.99,(dmg_st * 0.15 / (self.Armor.__dict__[Dmg.Type].val * (1 - Dmg.Ignore) * min(1,self.EquippedArmor.general.strength[0]/self.EquippedArmor.general.strength[1] + 0.25) if self.EquippedArmor.general.strength[0] != float('inf') else 1))**0.365 * dmg_st))

        if  self.EquippedArmor.general.strength[0] == 0: 
            self.EquippedArmor.general.fracture = -1

        if self.EquippedArmor.general.strength[0] != float('inf'):
            self.EquippedArmor.general.strength[0] = max(0, self.EquippedArmor.general.strength[0] - (dmg_st**1.8 / self.EquippedArmor.cloth.__dict__[Dmg.Type]))

        if randint(0,100) > self.EquippedArmor.general.fracture and self.EquippedArmor.general.strength[0] <= 0:
            self.EquippedArmor.general.strength[0] = 0
            self.EquippedArmor.general.fracture = -1
            

        self.Health.GetDmg(dmg, Dmg.Type)
        self.Reset()
    
    def GetDmg_without_armor(self, Dmg: Damag):
        
        self.Health.GetDmg(Dmg.Dmg if Dmg.Crit == None else Dmg.Crit, Dmg.Type)

    def GetMed(self, Med: Medication):

        self.Health.GetMed(Med.RegenED + Med.RegenAmMax * self.Health.Hp_Max + Med.RegenAmHere * self.Health.Hp)

    def Equipped(self, clothing):
        from Thing.Thing import Thing
        clothing : Thing

        self.EquippedArmor = clothing

        self.Reset()
        
    def Reset(self):
        print(f'{self.EquippedArmor.cloth.limb} - {self.Armor.F}:{self.Armor.M}')
        self.Armor.Reset()

        self.Armor.F.ChangeFactorEd(self.EquippedArmor.cloth.F * min(1,self.EquippedArmor.general.strength[0]/self.EquippedArmor.general.strength[1] + 0.25) if self.EquippedArmor.general.strength != None else 0)
        self.Armor.M.ChangeFactorEd(self.EquippedArmor.cloth.M * min(1,self.EquippedArmor.general.strength[0]/self.EquippedArmor.general.strength[1] + 0.25) if self.EquippedArmor.general.strength != None else 0)
        print(f'{self.EquippedArmor.cloth.limb} - {self.Armor.F}:{self.Armor.M}')

class VitalStat(_parameter):

    def __init__(self, HeadHp, LegHp, BodyHp, WingHp = 0, HornHp = 0) -> None:
        from Thing.Thing import all_clothing_to_creat

        super().__init__(1)

        self.Head   = Limb ( HeadHp)
        self.FLL    = Limb ( LegHp )
        self.FRL    = Limb ( LegHp )
        self.BLL    = Limb ( LegHp )
        self.BRL    = Limb ( LegHp )
        self.Body   = Limb ( BodyHp)
        self.RW = None
        self.LW = None
        self.Horn = None

        if WingHp != 0:
            
            self.RW = Limb(WingHp)
            self.LW = Limb(WingHp)
            self.RW.Equipped(all_clothing_to_creat['heading_RW'])
            self.LW.Equipped(all_clothing_to_creat['heading_LW'])

        if HornHp != 0:
            
            self.Horn = Limb(HornHp)
            self.Horn.Equipped(all_clothing_to_creat['heading_Horn'])

        self.Hp_Max = HeadHp + BodyHp + LegHp * 4
        self.Hp = HeadHp + BodyHp + LegHp * 4
        self.Hp_pct = self.Hp / self.Hp_Max


        self.Head.Equipped(all_clothing_to_creat['heading_Head'])
        self.FLL.Equipped(all_clothing_to_creat['heading_FLL'])  
        self.FRL.Equipped(all_clothing_to_creat['heading_FRL'])  
        self.BLL.Equipped(all_clothing_to_creat['heading_BLL'])  
        self.BRL.Equipped(all_clothing_to_creat['heading_BRL'])  
        self.Body.Equipped(all_clothing_to_creat['heading_Body'])

    def GetData(self):

        Data = ''

        if self.Horn != None:
            Data += 'Рог - '  + f"F-{self.Horn.Armor.F}/M-{self.Horn.Armor.M}"+ str(self.Horn.Health.Hp / self.Horn.Health.Hp_Max * 100) + '%\n'

        Data += 'Голова - '  + f"F-{self.Head.Armor.F}/M-{self.Head.Armor.M}"+ str(self.Head.Health.Hp / self.Head.Health.Hp_Max * 100) + '%\n'
        Data += '\n'
        Data += 'Тело - '    + f"F-{self.Body.Armor.F}/M-{self.Body.Armor.M}"+ str(self.Body.Health.Hp / self.Body.Health.Hp_Max * 100) + '%\n'
        if self.LW != None:
            Data += 'П Крыло - '    + f"F-{self.RW.Armor.F}/M-{self.RW.Armor.M}"+ str(self.RW.Health.Hp / self.RW.Health.Hp_Max * 100) + '%\n'
            Data += 'Л Крыло - '    + f"F-{self.LW.Armor.F}/M-{self.LW.Armor.M}"+ str(self.LW.Health.Hp / self.LW.Health.Hp_Max * 100) + '%\n'

        Data += '\n'
        Data += 'ЛП нога - ' + f"F-{self.FLL.Armor.F}/M-{self.FLL.Armor.M}"+ str(self.FLL.Health.Hp / self.FLL.Health.Hp_Max * 100) + '%\n'
        Data += 'ПП нога - ' + f"F-{self.FRL.Armor.F}/M-{self.FRL.Armor.M}"+ str(self.FRL.Health.Hp / self.FRL.Health.Hp_Max * 100) + '%\n'
        Data += 'ЛЗ нога - ' + f"F-{self.BLL.Armor.F}/M-{self.BLL.Armor.M}"+ str(self.BLL.Health.Hp / self.BLL.Health.Hp_Max * 100) + '%\n'
        Data += 'ПЗ нога - ' + f"F-{self.BRL.Armor.F}/M-{self.BRL.Armor.M}"+ str(self.BRL.Health.Hp / self.BRL.Health.Hp_Max * 100) + '%\n'
        

        Data += 'All - ' + str(self.Hp_pct * 100) + '%\n'

        return Data

    async def GetDmg(self, dmg: Damag):

        if dmg.Limb[0] == 'all':
            
            for key,limb in self.__dict__.items():

                if isinstance(limb,Limb) and not (key in dmg.Limb):

                    if dmg.Ignore == True:
                        limb.GetDmg_without_armor(dmg)

                    else:
                        limb.GetDmg(dmg)

            self.Update()
            return

        for limb in dmg.Limb:
            if dmg.Ignore:
                self.__dict__[limb].GetDmg_without_armor(dmg)

            else:    
                self.__dict__[limb].GetDmg(dmg)

        self.Update()
    
    async def GetMed(self, med: Medication):

        if med.Limb[0] == 'all':
            
            for key, limb in self.__dict__.items():

                if isinstance(limb,Limb) and not (key in med.Limb):

                    limb.GetMed(med)

            self.Update()
            return

        for limb in med.Limb:

            self.__dict__[limb].GetMed(med)

        self.Update()

    def HpReset(self):

        for limb in self.__dict__.values():

            if isinstance(limb,Limb):

                limb.Health.HpReset()

    def Update(self):

        self.Hp = 0
        self.Hp_Max = 0

        for limb in self.__dict__.values():

            if isinstance(limb,Limb):

                self.Hp += limb.Health.Hp
                self.Hp_Max += limb.Health.Hp_Max

                #limb.Update()


        
        self.Hp_pct = (self.Hp / self.Hp_Max).__round__(2)

    def Reset(self):
        print('__________')
        for limb in self.__dict__.values():
            
            if isinstance(limb,Limb):
                if limb.EquippedArmor.cloth.F == 9:
                    print(2)
                limb.Reset()

        self.Update()

    def Dress_don(self,object):

        for limb in self.__dict__.values():

            if isinstance(limb,Limb):

                if limb.EquippedArmor is object:

                    return True
        return False

class AttackData(_parameter):

    def __init__(self,WearFactorAm = 1,WearFactorEd = 0  , CritAttackChance = 2,CritAttackFactorAm = 2,AimedAttackFactor = 1,AttackFactor = 1,DamagFactorEd = 0, DamagFactorAm = 1, AimedApFactor = 0,ApFactor = 0) -> None:
        super().__init__(2)
        
        self.WearFactorAm = WearFactorAm
        self.WearFactorEd = WearFactorEd

        self.CritAttackChance = CritAttackChance 
        self.CritAttackFactorAm = CritAttackFactorAm

        self.AimedAttackFactor = AimedAttackFactor
        self.AttackFactor = AttackFactor

        self.DamagFactorEd = DamagFactorEd
        self.DamagFactorAm = DamagFactorAm

        self.AimedApFactor = AimedApFactor
        self.ApFactor = ApFactor

    def Reset(self):

        self.WearFactorAm = 1
        self.WearFactorEd = 0

        self.CritAttackChance = 10
        self.CritAttackFactorEd = 0
        self.CritAttackFactorAm = 2

        self.AimedAttackFactor = 1
        self.AttackFactor = 1

        self.DamagFactorEd = 0
        self.DamagFactorAm = 1

        self.AimedApFactor = 1
        self.ApFactor = 1

class ActionStat(_parameter):

    def __init__(self, special: Special) -> None:
        super().__init__(1)

        self.Ap_Max = Value(special.A.val / 2 + 5)
        self.Ap = Value(special.A.val / 2 + 5)
        self.Speed = Value(1)
        from Thing.Thing import Thing
        self.EquipedWeapon : Thing = None
        
        self.AttackData = AttackData()

    def GetDmg(self, attack_type: str, target: list[str],Forward: str, S = None) -> Damag: 
        from Thing.Thing import ThingAttackData
        data_thing : ThingAttackData = self.EquipedWeapon.weapon.__dict__[attack_type]

        if attack_type == 'melee' or attack_type == 'quit':
            dmg = self.EquipedWeapon.general.weight * S
        else:
            dmg = data_thing.dmg

        dmg = (dmg + (self.AttackData.DamagFactorEd + data_thing.DamagFactorEd)) * (self.AttackData.DamagFactorAm + data_thing.DamagFactorAm)

        if randint(1,100) < (self.AttackData.CritAttackChance + data_thing.CritAttackChanceFactorEd) * data_thing.CritAttackChanceFactorAm:
            crit = dmg * (self.AttackData.CritAttackFactorAm + data_thing.CritAttackFactorAm )
        else:
            crit = None

        return Damag(Limb = target, Dmg = dmg, Crit = crit, Type = data_thing.dmg_type, Weapon = self.EquipedWeapon.general.type, Forward = Forward)

    def Attack(self, attack_type: str, target: list[str],Forward: str, S, chance) -> list[Damag]:

        Dmg = self.GetDmg(attack_type, target, Forward, S)

        n = self.EquipedWeapon.weapon.__dict__[attack_type].number_of_strokes

        if attack_type in ['range','queue']:

            self.EquipedWeapon.general.magazine[0] -= n

        Dmg.Chance = chance

        Dmg.buff_after = self.EquipedWeapon.weapon.__dict__[attack_type].enemy_buff_after
        Dmg.buff_before = self.EquipedWeapon.weapon.__dict__[attack_type].enemy_buff_before

        if attack_type == 'melee' or attack_type == 'quit':
            dmg = self.EquipedWeapon.general.weight * S
        else:
            dmg = self.EquipedWeapon.weapon.__dict__[attack_type].dmg

        self.EquipedWeapon.general.strength[0] -= ((dmg + self.AttackData.WearFactorEd + self.EquipedWeapon.weapon.range.WearFactorEd) * (self.EquipedWeapon.weapon.range.WearFactorAm + self.AttackData.WearFactorAm)) * n

        if self.EquipedWeapon.general.strength[0] < 0 : 
            self.EquipedWeapon.general.strength[0] = 0

        if randint(0,100) > self.EquipedWeapon.general.fracture and self.EquipedWeapon.general.strength[0] == 0:
            self.EquipedWeapon.general.fracture = -1

        return [Dmg] * n 
        
    def Reset(self):

        self.AttackData.Reset()

    def Pick_up(self, object):

        self.EquipedWeapon = object

    def Handler(self,buff):

        if buff['id'] == ['Ap_Max','Ap','Speed']:

            self.__dict__[buff['id'][0]] += buff['n']

        else:

            self.__dict__[buff['id'][0]].__dict__[buff['id'][0]] += buff['n']

def StartVitalStat(Special: Special, race):

    start_hp = 5

    if race == 'pegasus':
        start_hp += 4

    elif race == 'changeling':
        start_hp -= 1

    elif race == 'griffin':
        start_hp += 8

    elif race == 'unicorn':
        pass

    elif race in ['pony', 'zebra']:
        start_hp += 6

    
    hp = Special.S.val + start_hp + Special.E.val *2 

    vital_stat = VitalStat(
        HeadHp  = hp,
        LegHp   = hp * 1.2,
        BodyHp  = hp * 1.5,
        WingHp  = hp if race in ['pegasus','changeling','griffin'] else 0,
        HornHp  = hp if race in ['unicorn','changeling'] else 0
    )

    

    return vital_stat

class Inventory(_parameter):
    def __init__(self, *arg) -> None:
        from Thing.Thing import Thing

        super().__init__(1)
        self.catalog : list[Thing]= []


    def Append(self, *arg) -> None:
        for thing in arg:
            self.catalog.append(thing)
            
    def Del(self, *arg):
        for thing in arg:
            self.catalog.pop(self.catalog.index(thing))

    def GetItem(self, id):

        self.catalog.sort(key =lambda x: x.general.id == id)

        return self.catalog[-1]

    async def Throw_out(self, id):

        self.catalog.sort(key =lambda x: x.general.id == id)

        self.catalog.pop(-1)


