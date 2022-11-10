from Data_classes.character import Character
from Thing.Thing import Thing

def GetArmor(ch: Character):
    VData = ch.VitalStat
    

    Data = ''

    if VData.Horn != None:
        Data += 'Рог - ' + f"{VData.Horn.Health.Hp / VData.Horn.Health.Hp_Max * 100}% | "+ f"F - {VData.Horn.Armor.F} / M - {VData.Horn.Armor.M}\n"
    Data += 'Голова - ' + f"{VData.Head.Health.Hp / VData.Head.Health.Hp_Max * 100}% | "+ f"F - {VData.Head.Armor.F} / M - {VData.Head.Armor.M}\n"
    Data += '\n' 
    Data += 'Тело - ' + f"{VData.Body.Health.Hp / VData.Body.Health.Hp_Max * 100}% | " + f"F - {VData.Body.Armor.F} / M - {VData.Body.Armor.M}\n"
    if VData.LW != None:
        Data += 'П Крыло - ' + f"{VData.RW.Health.Hp / VData.RW.Health.Hp_Max * 100}% | " + f"F - {VData.RW.Armor.F} / M - {VData.RW.Armor.M}\n"
        Data += 'Л Крыло - ' + f"{VData.LW.Health.Hp / VData.LW.Health.Hp_Max * 100}% | " + f"F - {VData.LW.Armor.F} / M - {VData.LW.Armor.M}\n"
    Data += '\n'
    Data += 'ЛП нога - ' + f"{VData.FLL.Health.Hp / VData.FLL.Health.Hp_Max * 100}% | " + f"F - {VData.FLL.Armor.F} / M - {VData.FLL.Armor.M}\n"
    Data += 'ПП нога - ' + f"{VData.FRL.Health.Hp / VData.FRL.Health.Hp_Max * 100}% | " + f"F - {VData.FRL.Armor.F} / M - {VData.FRL.Armor.M}\n"
    Data += 'ЛЗ нога - ' + f"{VData.BLL.Health.Hp / VData.BLL.Health.Hp_Max * 100}% | " + f"F - {VData.BLL.Armor.F} / M - {VData.BLL.Armor.M}\n"
    Data += 'ПЗ нога - ' + f"{VData.BRL.Health.Hp / VData.BRL.Health.Hp_Max * 100}% | " + f"F - {VData.BRL.Armor.F} / M - {VData.BRL.Armor.M}\n"
    Data += '\n'
    Data += 'Общий - ' + str(VData.Hp_pct * 100) + '%\n'    

    return Data

def GetWeapon(ch: Character):

    WData = ch.ActionStat.EquipedWeapon

    Data = ''

    if WData != None:

        Data += f"{WData.general.name}\n"
        Data += f"{WData.general.desp}\n"
        Data += f"Стоимость - {WData.general.cost}\n"
        if WData.general.magazine != None:
            Data += f"Магазин - {WData.general.magazine}\n"
        Data += f"Прочность - {WData.general.strength}"
        if WData.general.strength[0] / WData.general.strength[1] < 0.1:
            Data += ' | Скоро сломается!\n'
        Data += '\n'
        
        Data += f"Вес - {WData.general.weight}\n"

    else:
        Data += f"Твоя собственная конечность.\n Ты и так все о ней знаешь"


    return Data

def GetItemData(item: Thing):

    data = ''

    data += f'Прочность :{item.general.strength[0]}/{item.general.strength[1]}\n'
    data += f'Шанс разрущения: {100 - item.general.fracture.__round__(3)}%\n'
    data += f'Стоимость :{item.general.cost}\n'
    data += f'Вес :{item.general.weight}\n'
    data += f'Особености :{item.general.type}\n'
    if item.general.magazine != None:
        data += f'Магазин :{item.general.magazine[0]}/{item.general.magazine[1]}'

    return data