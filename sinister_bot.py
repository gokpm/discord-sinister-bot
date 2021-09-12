'''
Version:            0.2
Date last modified: 11-09-2021
Contributed by:     @icemelting, @Sygmus-1897, @Lazycl0ud
'''

import discord
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv

from utils.readWriteDB import *
from constants.emoji_unicodes import *


load_dotenv()


# -- Logger Initialization --
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# --- global variable declaration ---
token = os.environ['BOT_TOKEN']
id_guild = prefix_guild = channel_guild = dict_db_guild = None


# --- global variable initialization method --- 
def getPrefix (client, message):
    global id_guild, prefix_guild, channel_guild, dict_db_guild
    if (id_guild != str(message.guild.id)):
        id_guild = str(message.guild.id)
        checkAndCreateDB()
        dict_db_guild = readDB()
        if (id_guild not in dict_db_guild):
            dict_db_guild[id_guild] = { "prefix": "/sc", "channel": "any" }
            writeDB(dict_db_guild)
        prefix_guild = dict_db_guild[id_guild]["prefix"]
        channel_guild = dict_db_guild[id_guild]["channel"]
    return prefix_guild


# --- client object initialization ---
client = commands.Bot(command_prefix = getPrefix)


# --- on_ready and on_message ---
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not id_guild:
        getPrefix(0, message)    
    if message.content.startswith('?channel'):
        await showChannel(message)
    if message.content.startswith('?reset prefix'):
        await resetPrefix(message)
    if message.content.startswith('?reset channel'):
        await resetGuildChannel(message)       
    if message.content.startswith('?prefix'):
        await showPrefix(message)
    await client.process_commands(message)


# --- Indepedent Commands (i.e. Not Dependent on Server Prefix) ---
async def showChannel(message):
    channel_name = 'any'
    for channel in message.guild.channels:
        if (channel_guild == str(channel.id)):
            channel_name = channel.name
    embed_var = discord.Embed(title="Set Channel:", description=channel_name, color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)

async def resetPrefix(message):
    default_prefix_guild = '/sc'
    dict_db_guild.update({ id_guild: { 'prefix': default_prefix_guild, 'channel': default_prefix_guild }})
    writeDB(dict_db_guild)
    updateGlobalVariables()
    await react(1, message)

async def resetGuildChannel(message):
    default_channel = 'any'
    dict_db_guild.update({ id_guild: { 'prefix': prefix_guild, 'channel': default_channel }})
    writeDB(dict_db_guild)
    updateGlobalVariables()
    await react(1, message)

async def showPrefix(message):
    embed_var = discord.Embed(title="Prefix:", description=dict_db_guild[id_guild]['prefix'], color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)


# --- Dependent Commands (i.e. Dependent on Server Prefix) ---
@client.command()
async def clear(ctx, *, amount = 10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def hello(ctx): 
    embed_var = discord.Embed(description='Hi', color=8388640)
    await ctx.channel.send(embed=embed_var)
    await react(1, ctx.message)


## --- Grouped Commands (Set Prefix and Set Channel) ---
@client.group(aliases=['set'], invoke_without_subcommand=True)
async def _set(ctx):
    pass

@_set.command(aliases=['prefix'])
async def setPrefix(ctx):
    if channel_guild == str(ctx.message.channel.id) or channel_guild == 'any':
        words_message_content = ctx.message.content.split()
        if len(words_message_content) > 2:
            new_prefix_guild = words_message_content[2]
            if (new_prefix_guild == prefix_guild):
                await ctx.message.channel.send("Change Aborted: New Prefix is same as Old Prefix!")
                await react(0, ctx.message)
            else:
                dict_db_guild.update({ id_guild: {'prefix': new_prefix_guild, 'channel': channel_guild }})
                writeDB(dict_db_guild)
                updateGlobalVariables()
                await react(1, ctx.message)
        else: 
            await ctx.message.channel.send("Please provide the new prefix!")
            await react(0, ctx.message)
    else: 
        await ctx.message.channel.send("This channel is not supported!")
        await react(0, ctx.message)

@_set.command(aliases=['channel'])
async def setGuildChannel(ctx):
    words_message_content = ctx.message.content.split()
    set_channel_guild = words_message_content[2]
    for iter_channel in ctx.message.guild.channels:
        if ((set_channel_guild == str(iter_channel.id)) and (str(type(iter_channel)) == '<class \'discord.channel.TextChannel\'>')):
            dict_db_guild.update({ id_guild: { 'prefix': prefix_guild, 'channel': set_channel_guild }})
            writeDB(dict_db_guild)
            updateGlobalVariables()
            embed_var = discord.Embed(description='Channel Set', color=8388640)
            await ctx.message.channel.send(embed=embed_var)
    await react(1, ctx.message)


# --- Helper Functions ---
async def react(k, message):
    if k>0:
        await message.add_reaction(THUMBS_UP)
    else:
        await message.add_reaction(THUMBS_DOWN)

def updateGlobalVariables():
    global prefix_guild, channel_guild
    dict_new_db_guild = readDB()
    prefix_guild = dict_new_db_guild[id_guild]["prefix"]
    channel_guild = dict_new_db_guild[id_guild]["channel"]


#main
client.run(token)
