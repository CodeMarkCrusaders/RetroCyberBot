import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord import SelectOption
from Data_classes.Data_user import User
from Data_classes.character import Character


def list_race(SelectedValue):

    source = 'race!'

    options = [
        SelectOption(
            label = 'Пони',
            value = source + 'pony',
            default = SelectedValue == 'pony'
        ),
        SelectOption(
            label = 'Пегас',
            value = source + 'pegasus',
            default = SelectedValue == 'pegasus'
        ),
        SelectOption(
            label = 'Единорог',
            value = source + 'unicorn',
            default = SelectedValue == 'unicorn'
        ),
        SelectOption(
            label = 'Зебра',
            value = source + 'zebra',
            default = SelectedValue == 'zebra'
        ),
        SelectOption(
            label = 'Грифон',
            value = source + 'griffin',
            default = SelectedValue == 'griffin'
        ),
        SelectOption(
            label = 'Чейнджлинг',
            value = source + 'changeling',
            default = SelectedValue == 'changeling'
        )
    ]

    return options

def list_gender(SelectedValue):

    source = 'gender!'

    options = [
        SelectOption(
            label = 'Мужской',
            value = source + 'man',
            default = SelectedValue == 'man'
        ),
        SelectOption(
            label = 'Женский',
            value = source + 'woman',
            default = SelectedValue == 'woman'
        )
    ]

    return options
