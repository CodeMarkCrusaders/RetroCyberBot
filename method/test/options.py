import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord import SelectOption


def special_list(slc):

    options = [
        SelectOption(
            label = 'S',
            default = 'S' == slc
        ),
        SelectOption(
            label = 'P',
            default = 'P' == slc
        ),
        SelectOption(
            label = 'E',
            default = 'E' == slc
        ),
        SelectOption(
            label = 'C',
            default = 'C' == slc
        ),
        SelectOption(
            label = 'I',
            default = 'I' == slc
        ),
        SelectOption(
            label = 'A',
            default = 'A' == slc
        ),
        SelectOption(
            label = 'L',
            default = 'L' == slc
        )
    ]

    return options


def ability_list(slc):

    name = ['science',
        'medicine',
        'repair',
        'barter',
        'speech',
        'lockpick',
        'energy_weapons',
        'explosives',
        'throwing',
        'melee_weapons',
        'big_guns',
        'unarmed',
        'small_guns',
        'sneak',
        'fly',
        'magic'
    ]

    options = []

    for n in name:

        options.append(
            SelectOption(
                label = n,
                default = slc == n
            )
        )

    return options

def Vital_list(slc):

    options = [
        SelectOption(
            label = 'Head',
            default = 'Head' == slc
        ),
        SelectOption(
            label = 'Body',
            default = 'Body' == slc
        ),
        SelectOption(
            label = 'FLL',
            default = 'FLL' == slc
        ),
        SelectOption(
            label = 'FRL',
            default = 'FRL' == slc
        ),
        SelectOption(
            label = 'BLL',
            default = 'BLL' == slc
        ),
        SelectOption(
            label = 'BRL',
            default = 'BRL' == slc
        ),
    ]

    return options