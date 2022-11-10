from discord import Message
from discord.ext import commands
from Data_classes.all_user import AllUser
import asyncio
from screen import Screen
from Data_classes.Data_user import User
from discord import Interaction, InputTextStyle ,Embed
from discord.ui import Modal, InputText
import discord


TOKEN = 'OTYyODMyMTkyNjAwNDMyNjcw.YlNRWw.1-yL012kr8Ly9N5Uqq2zyx_Wl8w'
bot = commands.Bot(command_prefix = '!')


@bot.event
async def on_message(message: Message):

    id_author = message.author.id
    data = message.content

    if message.author == bot.user:

        pass

    else:
            
        screen = AllUser.Availability(id_author)

        if  data[0] == '!':

            data = data.split('!')[1]

            if data == 'start':

                await screen.Show('menu')

                await message.channel.send(embed = screen.Embed, view = screen) 
                
            elif data == 're':

                await message.channel.send(embed = screen.Embed, view = screen) 

            elif data == 'save':

                if screen.ControlUser.SelectedCharacter != None:

                    answer = screen.ControlUser.Save('All')

                    await message.channel.send(content = answer) 

                    await message.channel.send(embed= screen.Embed, view = screen)

                else:

                    await message.channel.send(content = 'Ошибка') 

        else:
            
            answer = screen.ControlUser.SetValue(Value = data)

            await screen.Update()

            if answer == '1':

                await message.channel.send(embed = screen.Embed, view = screen) 

            else:

                await message.channel.send(content = answer)


loop = asyncio.get_event_loop()
loop.create_task(bot.run(TOKEN))
#loop.create_task(Update())
loop.run_forever()