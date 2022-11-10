import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from discord import SelectOption
from Data_classes.stat import Inventory


def scroll(inventory: Inventory, n, default):

    options = []

    ln = len(inventory.catalog) // 20 if (len(inventory.catalog) / 20)%1 == 0 or len(inventory.catalog) < 20 else (len(inventory.catalog) // 20 + 1)
    if n != 0:
        options.extend = [
            SelectOption(
                label = 'В начало',
                value = '@0'
            ),
            SelectOption(
                label = '@˄',
                value = f'{n-1}',

            )
        ]
    g = 0
    while g < 21 and g + ln * 20 != len(inventory.catalog):
        options.append(
            SelectOption(
                label = inventory.catalog[g].general.name,
                #description = inventory.catalog[g].general.desp
                value = f"{inventory.catalog[g].general.id}"
            )
        )
        g+=1

    if n != ln:
        options.extend(
            [
                SelectOption(
                    label = '@˅',
                    value = f"{n + 1}"
                ),
                SelectOption(
                    label = 'В конец',
                    value = f'@{ln}'
                )
            ]
        )

    return options