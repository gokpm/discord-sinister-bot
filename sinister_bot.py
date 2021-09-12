'''
Date last modified: 12-09-2021
Contributed by:     @icemelting, @Sygmus-1897, @Lazycl0ud
'''

import discord
import logging
import os
import asyncpraw
from discord.ext import commands
from dotenv import load_dotenv

from utils.readWrite import *
from utils.clashofclansrecruit import *
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
prefix_bot = '/sc'
channel_bot = 'any'

checkAndCreateDB()

# --- global variable initialization method --- 
def getPrefix(client, message):
    global id_guild, prefix_guild, channel_guild
    id_guild = str(message.guild.id)
    prefix_guild = dict_db_guild[id_guild]['prefix']
    channel_guild = dict_db_guild[id_guild]['channel']
    return prefix_guild


# --- client object initialization ---
client = commands.Bot(command_prefix = getPrefix)


# --- get the guild ID's during start up ---
async def getGuildsOnStartup():
    global dict_db_guild
    dict_db_guild = readDB()
    for i_guild in client.guilds:
        if (not (str(i_guild.id) in dict_db_guild)):
            dict_db_guild.update({ str(i_guild.id): { 'prefix': prefix_bot, 'channel': channel_bot } })
            writeDB(dict_db_guild)
    return


# --- client events ---
@client.event
async def on_ready():
    await getGuildsOnStartup()
    print('We have logged in as {0.user}'.format(client))
    return
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
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
    return
    
@client.event
async def on_guild_join(guild):
    id_guild = str(guild.id)
    dict_db_guild.update( { id_guild: { 'prefix': prefix_bot, 'channel': channel_bot } } )
    writeDB(dict_db_guild)
    return
    
@client.event
async def on_guild_remove(guild):
    id_guild = str(guild.id)
    dict_db_guild.pop(id_guild)
    writeDB(dict_db_guild)
    return


# --- Indepedent Commands (i.e. Not Dependent on Server Prefix) ---
async def showChannel(message):
    channel_name = 'any'
    for channel in message.guild.channels:
        if (channel_guild == str(channel.id)):
            channel_name = channel.name
    embed_var = discord.Embed(title="Set Channel:", description=channel_name, color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)
    return

async def resetPrefix(message):
    dict_db_guild.update({ id_guild: { 'prefix': prefix_bot, 'channel': channel_guild}})
    writeDB(dict_db_guild)
    updateGlobalVariables()
    await react(1, message)
    return

async def resetGuildChannel(message):
    dict_db_guild.update({ id_guild: { 'prefix': prefix_guild, 'channel': channel_bot }})
    writeDB(dict_db_guild)
    updateGlobalVariables()
    await react(1, message)
    return

async def showPrefix(message):
    embed_var = discord.Embed(title="Prefix:", description=dict_db_guild[id_guild]['prefix'], color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)
    return


# --- Dependent Commands (i.e. Dependent on Server Prefix) ---
@client.command()
async def clear(ctx, *, amount = 10):
    await ctx.channel.purge(limit=amount)
    return

@client.command()
async def hello(ctx): 
    embed_var = discord.Embed(description='Hi', color=8388640)
    await ctx.channel.send(embed=embed_var)
    await react(1, ctx.message)
    return


# --- Commands to skip ---
@client.command()
async def channel(ctx): 
    pass
    
@client.command()
async def prefix(ctx): 
    pass
    
@client.command()
async def reset(ctx): 
    pass


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
    return

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
    return


# --- Helper Functions ---
async def react(k, message):
    if k>0:
        await message.add_reaction(THUMBS_UP)
    else:
        await message.add_reaction(THUMBS_DOWN)
    return

def updateGlobalVariables():
    global prefix_guild, channel_guild
    dict_new_db_guild = readDB()
    prefix_guild = dict_new_db_guild[id_guild]["prefix"]
    channel_guild = dict_new_db_guild[id_guild]["channel"]
    return

# --- main ---
client.loop.create_task(scoutReport(client))
client.run(token)
