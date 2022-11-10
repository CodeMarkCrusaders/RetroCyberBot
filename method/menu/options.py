import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord import SelectOption
from Data_classes.Data_user import User
from Data_classes.character import Character

gender = {
    'man'   : 'Мужской',
    'woman' : 'Женский',

}

race = {
    'pony'      :'Пони',
    'pegasus'   :'Пегас',
    'unicorn'   :'Единорог',
    'zebra'     :'Зебра',
    'griffin'   :'Грифон',
    'changeling':'Чейнджлинг',
    
}

def list_character(user: User): 

    options = []

    if len(user.CharacterList) != 0:

        CharacterList : list = user.GetAllChar()

        for char in CharacterList:

            char: Character

            basic_inf = char.GetBasicData()

            label = str(basic_inf['name'])

            description = 'Уровень: {name}, Расса: {race}, Пол: {gender}'.format(
                name    = basic_inf['lvl'],
                race    = race.setdefault(basic_inf['race']),
                gender  = gender.setdefault(basic_inf['gender'])
            )
            value = str(char.GetID())

            options.append(
                SelectOption(
                    label = label,
                    description = description,
                    value = value
                )
            )
    else:
        
        options.append(
            SelectOption(
                label = 'Пусто 🗋',
                value = 'pass'
            )
        )

        options.append(
            SelectOption(
                label = 'Создать персонажа',
                value = 'creat'
            )
        )
    
    return options