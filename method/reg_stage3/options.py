import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord import SelectOption

def list_traits(SelectedTraits):

    SelectedTrait1 = SelectedTraits['trait_1']
    SelectedTrait2 = SelectedTraits['trait_2']


    options = [
        [
            'Добрая душа',
            "+10 к всем не боевым и -10 к боевым навыкам",
            'kind_soul',
        ],
        [
            'Камикадзе',
            "+1 к ОД, получаемый урон увеличен на 2",
            'kamikaze',
        ],
        [
            'Создан разрушать',
            "+5 % к шансу критического урона.\n +15 % к скорости износа снаряжения",
            'created_to_destroy',
        ],
        [
            'Стрельба навскидку',
            "Стрельба требует на 1 очко меньше, невозможна прицельная стрельба",
            'shooting_offhand',
        ],
        [
            'Техника спуска',
            "Прицельная стрельба стоит на 1 очко меньше.\nСтрельба очередями невозможна.",
            'escape_technique',
        ],
        [
            'Тяжёлая рука',
            "+6 урона в ближнем бою.\n Все Атаки в ближнем бою стоят на 1 очко больше.",
            'heavy_hand',
        ],
        [
            'Четыре глаза',
            "+2 ВСП при ношении любых очков, -1 к базовому Восприятию",
            'four_eyes',
        ],
        [
            'Шустрик',
            "+1 ЛОВ. Скорость увеличиная на 2 метра. Урон конечностям увеличен на 15%",
            'quick',
        ],
        [
            'Горячая кровь',
            "+45 % урона и -2 к ВСП и ИНТ при ОЗ ниже 50%",
            'hot_blood',
        ],
        [
            'Тренированный',
            "+8 очков ко всем навыкам, -10 % к получаемому опыту",
            'trained',
        ],
    ]
    list_traits_1 =[
        SelectOption(
            label = 'Ничего',
            description = "+0 к всем характиристикам",
            value = 'trait_1!None',
            default = 'None' == SelectedTrait1
        ),
    ]
    list_traits_2 = [
        SelectOption(
            label = 'Ничего',
            description = "+0 к всем характиристикам",
            value = 'trait_2!None',
            default = 'None' == SelectedTrait2
        ),
    ]

    if SelectedTrait1 == 'shooting_offhand':

        list_traits_1.append(
            SelectOption(
                label = options[4][0],
                description = options[4][1],
                value = 'trait_1!' + options[4][2],
                default = False
            )
        )
        options.pop(4)
    elif SelectedTrait2 == 'shooting_offhand':
        list_traits_2.append(
            SelectOption(
                label = options[4][0],
                description = options[4][1],
                value = 'trait_2!' + options[4][2],
                default = False
            )
        )
        options.pop(4)

    elif SelectedTrait1 == 'escape_technique':
        list_traits_1.append(
            SelectOption(
                label = options[3][0],
                description = options[3][1],
                value = 'trait_1!' + options[3][2],
                default = False
            )
        )
        options.pop(3)
    elif SelectedTrait2 == 'escape_technique':
        list_traits_2.append(
            SelectOption(
                label = options[3][0],
                description = options[3][1],
                value = 'trait_2!' + options[3][2],
                default = False
            )
        )
        options.pop(3)

    for option in options:
            
        if SelectedTrait1 == option[2]:

            list_traits_1.append(
                SelectOption(
                    label = option[0],
                    description = option[1],
                    value = 'trait_1!' + option[2],
                    default = True
                )
            )

        elif SelectedTrait2 == option[2]:

            list_traits_2.append(
                SelectOption(
                    label = option[0],
                    description = option[1],
                    value = 'trait_2!' + option[2],
                    default = True
                )
            )

        else:

            list_traits_1.append(
                SelectOption(
                    label = option[0],
                    description = option[1],
                    value = 'trait_1!' + option[2],
                    default = False
                )
            )

            list_traits_2.append(
                SelectOption(
                    label = option[0],
                    description = option[1],
                    value = 'trait_2!' + option[2],
                    default = False
                )
            )

    return list_traits_1, list_traits_2