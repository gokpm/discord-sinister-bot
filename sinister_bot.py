'''
Version:            0.2
Date last modified: 10-09-2021
Contributed by:     @icemelting, @Sygmus-1897, @Lazycl0ud
'''

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from utils.db_operations import *
from constants.emoji_unicodes import *

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = os.environ['BOT_TOKEN']

global prefix_dict

def getPrefix (_, message):
    server_id = str(message.guild.id)
    prefix_db_fp = 'server_prefix_db.json'

    if (not os.path.isfile(prefix_db_fp)):
        writeDB({ server_id: { "prefix": "/sc", "channel": "any" } })
    
    prefix_dict = readDB()
    
    if (server_id not in prefix_dict):
        prefix_dict[server_id] = { "prefix": "/sc", "channel": "any" }
        writeDB(prefix_dict)

    return prefix_dict[server_id]["prefix"]


client = commands.Bot(command_prefix = getPrefix)

async def react(k, message):
    if k>0:
        await message.add_reaction(THUMBS_UP)
    else:
        await message.add_reaction(THUMBS_DOWN)

# @client.event
# async def on_message(message):
#     global prefix, bot, set_channel
#     i = 0

#     if message.author == client.user:
#         return
#     else:
#         id_server = str(message.guild.id)
#         if id_server in dict_prefix:
#             prefix = dict_prefix[id_server]['prefix']
#             set_channel = dict_prefix[id_server]['channel']

#     if message.content.startswith(prefix+'set channel'):
#         words = message.content.split()
#         set_channel = words[2]
#         for every_channel in message.guild.channels:
#             if ((set_channel == str(every_channel.id)) and (str(type(every_channel)) == '<class \'discord.channel.TextChannel\'>')):
#                 dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
#                 with open(filepath_db_prefix, 'w') as db_prefix:
#                     json.dump(dict_prefix, db_prefix, indent = 4)
#                     db_prefix.close
#                 embed_var = discord.Embed(description='Channel Set', color=8388640)
#                 await message.channel.send(embed=embed_var)
#                 i += 1
#         await react(i, message)
        
#     if message.content.startswith('?channel'):
#         name_channel = 'Any'
#         for every_channel in message.guild.channels:
#             if (set_channel == str(every_channel.id)):
#                 name_channel = every_channel.name
#         embed_var = discord.Embed(title="Set Channel:", description=name_channel, color=8388640)
#         await message.channel.send(embed=embed_var)
#         i += 1
#         await react(i, message)
#         return

#     if message.content.startswith('?reset prefix'):
#         prefix = '/sc'
#         dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
#         with open(filepath_db_prefix, 'w') as db_prefix:
#             json.dump(dict_prefix, db_prefix, indent = 4)
#             db_prefix.close
#         i += 1
#         await react(i, message)

#     if message.content.startswith('?reset channel'):
#         set_channel = 'any'
#         dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
#         with open(filepath_db_prefix, 'w') as db_prefix:
#             json.dump(dict_prefix, db_prefix, indent = 4)
#             db_prefix.close
#         i += 1
#         await react(i, message)
            
#     if set_channel == str(message.channel.id) or set_channel == 'any':
#         if message.content.startswith(prefix+'set prefix'):
#             words = message.content.split()
#             if len(words) > 2:
#                 prefix = words[2]
#                 dict_prefix.update({id_server: {'prefix':prefix, 'channel':set_channel}})
#                 with open(filepath_db_prefix, 'w') as db_prefix:
#                     json.dump(dict_prefix, db_prefix, indent = 4)
#                     db_prefix.close
#                 i += 1
#             await react(i, message)
            
#         if message.content.startswith('?prefix'):
#             embed_var = discord.Embed(title="Prefix:", description=prefix, color=8388640)
#             await message.channel.send(embed=embed_var)
#             i += 1
#             await react(i, message)
#             return

#         if message.content.startswith(prefix+'hello'):
#             embed_var = discord.Embed(description='Hi', color=8388640)
#             await message.channel.send(embed=embed_var)
#             i += 1
#             await react(i, message)
#     bot = commands.Bot(command_prefix=prefix)
#     return


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # await initcache()
    return

@client.command()
async def hello(ctx): 
    embed_var = discord.Embed(description='Hi', color=8388640)
    await ctx.channel.send(embed=embed_var)
    await react(1, ctx.message)

# def main():
    

# if __name__ == '__main__':
#     main()

client.run(token)