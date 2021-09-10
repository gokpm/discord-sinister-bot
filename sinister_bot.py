'''
Version:            0.1
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

token = <BOT TOKEN>
client = discord.Client()
filepath_db_prefix = 'db_prefix.json'

try:
    with open(filepath_db_prefix, 'r') as db_prefix:
        dict_prefix = json.load(db_prefix)
        db_prefix.close
    print(1)
except:
    with open(filepath_db_prefix, 'w') as db_prefix:
        json.dump({}, db_prefix, indent = 4)
        db_prefix.close
    with open(filepath_db_prefix, 'r') as db_prefix:
        dict_prefix = json.load(db_prefix)
        db_prefix.close
    print(2)
    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(3)

@client.event
async def on_message(message):
    print(4)
    global prefix, bot
    if message.author == client.user:
        print(5)
        return
    else:
        print(6)
        id_server = message.guild.id
        if str(id_server) in dict_prefix:
            print(7)
            prefix = dict_prefix[str(id_server)]['prefix']
        else:
            print(8)
            prefix = '/sc'
            dict_prefix.update({str(id_server): {'prefix':prefix}})
            with open(filepath_db_prefix, 'w') as db_prefix:
                json.dump(dict_prefix, db_prefix, indent = 4)
                db_prefix.close
    print(9)
    if message.content.startswith(prefix+'prefix'):
        print(10)
        words = message.content.split()
        prefix = words[1]
        dict_prefix.update({str(id_server): {'prefix':prefix}})
        with open(filepath_db_prefix, 'w') as db_prefix:
            json.dump(dict_prefix, db_prefix, indent = 4)
            db_prefix.close
        await message.add_reaction('\U0001f44d')
    bot = commands.Bot(command_prefix=prefix)
    print(11)
    if message.content.startswith('?prefix'):
        print(12)
        embed_var = discord.Embed(title="Prefix:", description=prefix, color=8388640)
        await message.channel.send(embed=embed_var)
        await message.add_reaction('\U0001f44d')
    if message.content.startswith(prefix+'hello'):
        print(13)
        embed_var = discord.Embed(description='Hi', color=8388640)
        await message.channel.send(embed=embed_var)
        await message.add_reaction('\U0001f44d')

def main():
    client.run(token)

if __name__ == '__main__':
    main()
    


