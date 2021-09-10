'''
Version:            0.2
Date last modified: 10-09-2021
Contributed by:     @icemelting, @Sygmus-1897, @Lazycl0ud
'''

from discord.ext import commands
import discord
import logging
import json

print(0)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = <BOT_TOKEN>
client = discord.Client()

async def initcache():
    global dict_prefix, filepath_db_prefix
    filepath_db_prefix = 'db_prefix.json'
    try:
        with open(filepath_db_prefix, 'r') as db_prefix:
            dict_prefix = json.load(db_prefix)
    except:
        with open(filepath_db_prefix, 'w') as db_prefix:
            json.dump({}, db_prefix, indent = 4)
        with open(filepath_db_prefix, 'r') as db_prefix:
            dict_prefix = json.load(db_prefix)
    return dict_prefix

async def react(k, message):
    if k>0:
        await message.add_reaction('\U0001f44d')
    else:
        await message.add_reaction('\U0001f44e')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await initcache()
    return

@client.event
async def on_message(message):
    global prefix, bot, set_channel
    i = 0

    if message.author == client.user:
        return
    else:
        id_server = str(message.guild.id)
        if id_server in dict_prefix:
            prefix = dict_prefix[id_server]['prefix']
            set_channel = dict_prefix[id_server]['channel']
        else:
            prefix = '/sc'
            set_channel = 'any'
            dict_prefix.update({id_server: {'prefix':prefix, 'channel': set_channel}})
            with open(filepath_db_prefix, 'w') as db_prefix:
                json.dump(dict_prefix, db_prefix, indent = 4)

    if message.content.startswith(prefix+'set channel'):
        words = message.content.split()
        set_channel = words[2]
        for every_channel in message.guild.channels:
            if ((set_channel == str(every_channel.id)) and (str(type(every_channel)) == '<class \'discord.channel.TextChannel\'>')):
                dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
                with open(filepath_db_prefix, 'w') as db_prefix:
                    json.dump(dict_prefix, db_prefix, indent = 4)
                embed_var = discord.Embed(description='Channel Set', color=8388640)
                await message.channel.send(embed=embed_var)
                i += 1
        await react(i, message)
        
    if message.content.startswith('?channel'):
        name_channel = 'Any'
        for every_channel in message.guild.channels:
            if (set_channel == str(every_channel.id)):
                name_channel = every_channel.name
        embed_var = discord.Embed(title="Set Channel:", description=name_channel, color=8388640)
        await message.channel.send(embed=embed_var)
        i += 1
        await react(i, message)
        return

    if message.content.startswith('?reset prefix'):
        prefix = '/sc'
        dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
        with open(filepath_db_prefix, 'w') as db_prefix:
            json.dump(dict_prefix, db_prefix, indent = 4)
        i += 1
        await react(i, message)

    if message.content.startswith('?reset channel'):
        set_channel = 'any'
        dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
        with open(filepath_db_prefix, 'w') as db_prefix:
            json.dump(dict_prefix, db_prefix, indent = 4)
        i += 1
        await react(i, message)
            
    if set_channel == str(message.channel.id) or set_channel == 'any':
        
        if message.content.startswith(prefix+'set prefix'):
            words = message.content.split()
            prefix = words[2]
            dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
            with open(filepath_db_prefix, 'w') as db_prefix:
                json.dump(dict_prefix, db_prefix, indent = 4)
            i += 1
            await react(i, message)
            
        if message.content.startswith('?prefix'):
            embed_var = discord.Embed(title="Prefix:", description=prefix, color=8388640)
            await message.channel.send(embed=embed_var)
            i += 1
            await react(i, message)
            return

        if message.content.startswith(prefix+'hello'):
            embed_var = discord.Embed(description='Hi', color=8388640)
            await message.channel.send(embed=embed_var)
            i += 1
            await react(i, message)
    bot = commands.Bot(command_prefix=prefix)
    return

def main():
    client.run(token)

if __name__ == '__main__':
    main()
