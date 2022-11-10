from discord.ui import Select, Button
from discord import ButtonStyle, Embed, Interaction

def NumberButtonCreate(SelectedNumber ) -> list[Button]:

    NumberButtonList = []

    for number in range(1,5):
        NumberButtonList.append(Button(
           label = str(number),
           style = ButtonStyle.green if SelectedNumber == number else ButtonStyle.grey,
           custom_id = str(number),
           row = 2
        ))

    return NumberButtonList

        