'''
Version:            0.2
Date last modified: 11-09-2021
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


# -- Logger Initialization --
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = os.environ['BOT_TOKEN']


# --- global variable declaration ---
server_id = server_prefix = selected_channel = prefix_dict = None


# --- global variable initialization method --- 
def getPrefix (client, message):
    global server_id, server_prefix, selected_channel, prefix_dict

    if (server_id != str(message.guild.id)):
        server_id = str(message.guild.id)
        
        checkAndCreateDB(server_id)
        prefix_dict = readDB()
        
        if (server_id not in prefix_dict):
            prefix_dict[server_id] = { "prefix": "/sc", "channel": "any" }
            writeDB(prefix_dict)

        server_prefix = prefix_dict[server_id]["prefix"]
        selected_channel = prefix_dict[server_id]["channel"]

    return server_prefix


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

    if not server_id:
        getPrefix(0, message)
        
    if message.content.startswith('?channel'):
        await showChannel(message)

    if message.content.startswith('?reset prefix'):
        await resetPrefix(message)

    if message.content.startswith('?reset channel'):
        await resetChannel(message)
            
    if message.content.startswith('?prefix'):
        await sendPrefix(message)

    await client.process_commands(message)




# --- Indepedent Commands (i.e. Not Dependent on Server Prefix) ---
async def showChannel(message):
    channel_name = 'any'
    for channel in message.guild.channels:
        if (selected_channel == str(channel.id)):
            channel_name = channel.name
    embed_var = discord.Embed(title="Set Channel:", description=channel_name, color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)


async def resetPrefix(message):
    default_prefix = '/sc'
    prefix_dict.update({ server_id: { 'prefix': default_prefix, 'channel': default_prefix }})
    writeDB(prefix_dict)
    updateGlobalVariables()
    await react(1, message)


async def resetChannel(message):
    default_channel = 'any'
    prefix_dict.update({ server_id: { 'prefix': server_prefix, 'channel': default_channel }})
    writeDB(prefix_dict)
    updateGlobalVariables()
    await react(1, message)


async def sendPrefix(message):
    embed_var = discord.Embed(title="Prefix:", description=prefix_dict[server_id]['prefix'], color=8388640)
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
    if selected_channel == str(ctx.message.channel.id) or selected_channel == 'any':
        words = ctx.message.content.split()
        if len(words) > 2:
            new_prefix = words[2]
            if (new_prefix == server_prefix):
                await ctx.message.channel.send("Change Aborted: New Prefix is same as Old Prefix!")
                await react(0, ctx.message)
            else:
                prefix_dict.update({ server_id: {'prefix': new_prefix, 'channel': selected_channel }})
                writeDB(prefix_dict)
                updateGlobalVariables()
                await react(1, ctx.message)
        else: 
            await ctx.message.channel.send("Please provide the new prefix!")
            await react(0, ctx.message)
    else: 
        await ctx.message.channel.send("This channel is not supported!")
        await react(0, ctx.message)


@_set.command(aliases=['channel'])
async def setChannel(ctx):
    words = ctx.message.content.split()
    set_channel = words[2]
    for channel in ctx.message.guild.channels:
        if ((set_channel == str(channel.id)) and (str(type(channel)) == '<class \'discord.channel.TextChannel\'>')):
            prefix_dict.update({ server_id: { 'prefix': server_prefix, 'channel': set_channel }})
            writeDB(prefix_dict)
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
    global server_id, server_prefix, selected_channel
    new_prefix_dict = readDB()
    server_prefix = new_prefix_dict[server_id]["prefix"]
    selected_channel = new_prefix_dict[server_id]["channel"]




client.run(token)