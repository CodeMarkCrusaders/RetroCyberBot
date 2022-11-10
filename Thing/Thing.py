from copy import copy
from email import header
import sys
import os
import json

sys.path.append(os.path.dirname(sys.path[0]))
from Data_classes.stat import Clothing,Buff, Damag, Medication,Mod, Do,Triger, _parameter , general

p = 'Thing\\clothing_list'

def Attack(plan:dict):
    
    if plan == None:

        return ThingAttackData({})
        
    return ThingAttackData(plan)

def GetTriger(plan: dict):
    if plan == None:
        return None

    return {"OR" : tuple([Triger(field = tuple(triger['field']) if triger.get('field') != None else None , con = triger['con'],n = triger.get('n')) for triger in plan.get('OR',tuple())]),"AND" : tuple([Triger(field = tuple(triger['field']) if triger.get('field') != None else None , con = triger['con'],n = triger.get('n')) for triger in plan.get('AND',tuple())]), 'NOT': tuple([Triger(field = tuple(triger['field']) if triger.get('field') != None else None , con = triger['con'],n = triger.get('n')) for triger in plan.get('NOT',tuple())])}

def GetHeal(plan:list[dict]):
    if plan == None:
        return None

    return tuple([Medication(Limb = tuple(heal['limb']) , RegenED = float(heal.get('regen_ed', 0)), RegenAmHere = float(heal.get('regen_am_here', 0)), RegenAmMax = float(heal.get('regen_am_max', 0))) for heal in plan]),

def GetDmg(plan:list[dict]):
    if plan == None:
        return None

    return tuple([Damag(Limb = tuple(dmg['limb']), Dmg = float(dmg['dmg']), Type = dmg['type'], Crit = float(dmg.get('crit')), Ignore = dmg.get('ignore') if dmg.get('ignore', 0) == True else float(dmg.get('ignore'))) for dmg in plan.get('dmg', [])])

def GetMod(plan: list[dict]):
    if plan == None:
        return None

    return tuple([Mod(field = tuple(mod['field']), ed = mod.get('ed',True), n = mod['n']) for mod in plan])

def GetBuff(plan: list[dict]):
    from buff_list.buff import all_buff
    if plan == None:
        return None

    buff_list = []
    for buff in plan:
        if isinstance(buff,list):
            for buff_1 in buff:
                buff_list.append(all_buff[buff_1['id']])
        else:
            buff_list.append(Buff(name = buff['name'] ,desp = buff['desp'],id = buff['id'], triger = GetTriger(buff.get('triger')) , mod = GetMod(buff.get('mod')), heal = GetHeal(buff.get('heal')), dmg = GetDmg(buff.get('dmg'))))
    return buff_list

def GetClothing(data: dict):
    if data == None:
        return None
    list_buff = GetBuff(data['buff'])

    list_don_con = GetTriger(data.get('don_con'))

    clothing = Clothing(
        F = data['F'],
        M = data['M'],
        don_con = list_don_con,
        limb = data['limb'],
        buff = tuple(list_buff)
        )

    return clothing
    
def GetThing(path):
    with open(path) as outfile:
        data : dict = json.load(outfile)
    return Thing(data)

class Thing(_parameter):
    def __init__(self, path : str) -> None:
        with open(path,  encoding ='utf-8') as outfile:
            plan : dict = json.load(outfile,)
        self.general = general(plan['general'])
        self.cloth = GetClothing(plan.get('cloth'))
        self.weapon = ThingWeaponData(plan.get('weapon',{}))
        self.do = Do(plan.get('do'))
        super().__init__(3)

class ThingWeaponData():
    def __init__(self, plan) -> None:
        
        self.buff : tuple[Buff] = [Buff(name = buff['name'] ,desp = buff['desp'],id = buff['id'], triger = GetTriger(buff.get('triger')) , mod = GetMod(buff.get('mod')), heal = GetHeal(buff.get('heal')), dmg = GetDmg(buff.get('dmg'))) for buff in plan.get('buff', [])]
        self.don_con : tuple[Triger] = GetTriger(plan.get('don_con'))
        self.melee = Attack(plan.get('melee', {}))
        self.range = Attack(plan.get('range')) if plan.get('range') != None else None
        self.queue = Attack(plan.get('queue')) if plan.get('range') != None else None
        self.quit = Attack(plan.get('quit', {}))
        
class ThingAttackData():
    def __init__(self, plan: dict) -> None:

        self.WearFactorAm = float(plan.get('WearFactorAm', 0))
        self.WearFactorEd = float(plan.get('WearFactorEd', 0))

        self.CritAttackChanceFactorEd = float(plan.get("CritAttackChanceFactorEd", 0))
        self.CritAttackChanceFactorAm = float(plan.get("CritAttackChanceFactorAm", 1))
        self.CritAttackFactorAm = float(plan.get("CritAttackFactorAm", 0))

        self.AimedAttackFactor = float(plan.get("AimedAttackFactor", 0))
        self.AttackFactor = float(plan.get("AttackFactor", 0))

        self.DamagFactorEd = float(plan.get("DamagFactorEd", 0))
        self.DamagFactorAm = float(plan.get("DamagFactorAm", 0))

        self.AimedApFactor = float(plan.get('AimedApFactor', 0))
        self.ApFactor = float(plan.get('ApFactor', 0))

        self.enemy_buff_before = [Buff(name = buff['name'] ,desp = buff['desp'],id = buff['id'], triger = GetTriger(buff.get('triger')) , mod = GetMod(buff.get('mod')), heal = GetHeal(buff.get('heal')), dmg = GetDmg(buff.get('dmg'))) for buff in plan.get('enemy_buff_before',tuple())]
        self.enemy_buff_after = [Buff(name = buff['name'] ,desp = buff['desp'],id = buff['id'], triger = GetTriger(buff.get('triger')) , mod = GetMod(buff.get('mod')), heal = GetHeal(buff.get('heal')), dmg = GetDmg(buff.get('dmg'))) for buff in plan.get('enemy_buff_after',tuple())]

        self.dmg = plan.get('dmg') if plan.get('dmg') == None else float(plan.get('dmg'))
        self.number_of_strokes = int(plan.get('number_of_strokes', 1))
        self.dmg_type = plan.get('dmg_type', 'F')
        self.ability = plan.get('ability')

        self.distance = distance(plan.get('distance', {}))

class distance():
    def __init__(self, plan: dict[str:str]):

        self.back_to_back = float(plan.get('back_to_back', 1))
        self.close = float(plan.get('close', 0.85))
        self.medium = float(plan.get('medium', 0.7))
        self.far = float(plan.get('far', 0.3))
        self.over_long = float(plan.get('over_long', 0.05))


all_clothing_to_creat = {
    'black_glasses': Thing(p + "\\Head\\black_glasses.json"),
    'heading_Head': Thing(p + "\\Head\\heading_head.json"),
    'heading_Body': Thing(p + "\\Body\\heading_body.json"),
    'heading_BLL':  Thing(p + "\\Leg\\heading_BLL.json"),
    'heading_BRL':  Thing(p + "\\Leg\\heading_BRL.json"),
    'heading_FLL':  Thing(p + "\\Leg\\heading_FLL.json"),
    'heading_FRL':  Thing(p + "\\Leg\\heading_FRL.json"),
    'heading_RW':  Thing(p + "\\Wing\\heading_RW.json"),
    'heading_LW':  Thing(p + "\\Wing\\heading_LW.json"),
    'heading_Horn':  Thing(p + "\\Horn\\heading_horn.json"),
}
all_Med_to_creat = {
    'healing_potion': Thing("Thing\\med_list\\healing_potion.json"),
}
all_Weapon_to_creat = {
    "10mm_pistol" : Thing("Thing\\weapon_list\\pistol\\10mm_pistol.json")
}
all_item_to_creat = {}




class All_Item:
    def __init__(self) -> None:
        self.catalog = {}

    def Apend(self,id):
        n = len(self.catalog)
        self.catalog[n] = copy(all_item_to_creat[id])
        self.catalog[n].general.id = n

def g(f):
    for root, dirs, files in os.walk(f):  
        if '__pycache__' in root :
            continue
        for buff_paht in files:
            if buff_paht in ['Thing.py']:
                continue
            all_item_to_creat[buff_paht.split('.')[0]] = Thing(root +'\\'+ buff_paht)
            
g('Thing')
all_item = All_Item()
all_item.Apend('10mm_pistol')
all_item.Apend('black_glasses')
all_item.Apend('healing_potion')

print(1)