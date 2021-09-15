'''
Date last modified: 12-09-2021
Contributed by:     @icemelting, @Sygmus-1897
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
id_guild = prefix_guild = channel_guild = wc_guild = wm_guild = dict_db_guild = None
prefix_bot = '!'
channel_bot = wc_bot = wm_bot = 'N/A'

checkAndCreateDB()

# --- global variable initialization method --- 
def getGuildValues(client, message):
    global id_guild, prefix_guild, channel_guild, wc_guild, wm_guild
    id_guild = str(message.guild.id)
    prefix_guild = dict_db_guild[id_guild]['prefix']
    channel_guild = dict_db_guild[id_guild]['channel']
    wc_guild = dict_db_guild[id_guild]['welcome channel']
    wm_guild = dict_db_guild[id_guild]['welcome message']
    return prefix_guild


# --- Check if the set channel exists. If not, change the channel to bot defaults ---
async def channelCheck(message):
    if (channel_guild != channel_bot) or (wc_guild != wc_bot):
        i = 0
        j = 0
        for channel in message.guild.channels:
            if (channel_guild == str(channel.id)):
                i += 1
            elif (wc_guild == str(channel.id)):
                j += 1
        if i < 1:
            updateDB(new_channel = channel_bot)
        if j < 1:
            updateDB(new_wc = wc_bot)    
    return
            
# --- client object initialization ---
client = commands.Bot(command_prefix = getGuildValues)


# --- get the guild ID's during start up ---
async def getGuildsOnStartup():
    global dict_db_guild
    dict_db_guild = readDB()
    for i_guild in client.guilds:
        if (not (str(i_guild.id) in dict_db_guild)):
            updateDB(0, new_guild = str(i_guild.id))
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
    getGuildValues(0, message)
    await channelCheck(message)
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
    updateDB(0, new_guild = id_guild)
    return
    
@client.event
async def on_guild_remove(guild):
    id_guild = str(guild.id)
    dict_db_guild.pop(id_guild)
    writeDB(dict_db_guild)
    return


# --- Indepedent Commands (i.e. Not Dependent on Server Prefix) ---
async def showChannel(message):
    channel_name = channel_bot
    for channel in message.guild.channels:
        if (channel_guild == str(channel.id)):
            channel_name = channel.name
    embed_var = discord.Embed(title="Set Channel:", description=channel_name, color=8388640)
    await message.channel.send(embed=embed_var)
    await react(1, message)
    return

async def resetPrefix(message):
    if channel_guild == str(message.channel.id) or channel_guild == channel_bot:
        if message.author.guild_permissions.administrator:
            updateDB(new_prefix = prefix_bot)
            await react(1, message)
    return

async def resetGuildChannel(message):
    if channel_guild == str(message.channel.id) or channel_guild == channel_bot:
        if message.author.guild_permissions.administrator:
            updateDB(new_channel = channel_bot)
            await react(1, message)
    return

async def showPrefix(message):
    if channel_guild == str(message.channel.id) or channel_guild == channel_bot:
        embed_var = discord.Embed(title="Prefix:", description=dict_db_guild[id_guild]['prefix'], color=8388640)
        await message.channel.send(embed=embed_var)
        await react(1, message)
    return


# --- Dependent Commands (i.e. Dependent on Server Prefix) ---
@client.command()
async def clear(ctx, *, amount = 1):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount + 1)
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
    if channel_guild == str(ctx.message.channel.id) or channel_guild == channel_bot:
        if ctx.message.author.guild_permissions.administrator:
            words_message_content = ctx.message.content.split()
            if len(words_message_content) > 2:
                new_prefix_guild = words_message_content[2]
                if (new_prefix_guild == prefix_guild):
                    await ctx.message.channel.send("Change Aborted: New Prefix is same as Old Prefix!")
                    await react(0, ctx.message)
                else:
                    updateDB(new_prefix = new_prefix_guild)
                    await react(1, ctx.message)
            else: 
                await ctx.message.channel.send("Please provide the new prefix!")
                await react(0, ctx.message)
    return

@_set.command(aliases=['channel'])
async def setGuildChannel(ctx):
    if channel_guild == str(ctx.message.channel.id) or channel_guild == channel_bot:
        if ctx.message.author.guild_permissions.administrator:
            words_message_content = ctx.message.content.split()
            if len(words_message_content) > 2:
                set_channel_guild = words_message_content[2]
                for iter_channel in ctx.message.guild.channels:
                    if ((set_channel_guild == str(iter_channel.id)) and (str(type(iter_channel)) == '<class \'discord.channel.TextChannel\'>')):
                        updateDB(new_channel = set_channel_guild)
                        embed_var = discord.Embed(description='Channel Set', color=8388640)
                        await ctx.message.channel.send(embed=embed_var)
                await react(1, ctx.message)
    return
    
@_set.command(aliases=['wc'])
async def setWelcomeChannel(ctx):
    if channel_guild == str(ctx.message.channel.id) or channel_guild == channel_bot:
        if ctx.message.author.guild_permissions.administrator:
            words_message_content = ctx.message.content.split()
            if len(words_message_content) > 2:
                new_wc_guild = words_message_content[2]
                for iter_channel in ctx.message.guild.channels:
                    if ((new_wc_guild == str(iter_channel.id)) and (str(type(iter_channel)) == '<class \'discord.channel.TextChannel\'>')):
                        updateDB(new_wc = new_wc_guild)
                        embed_var = discord.Embed(description='Channel Set', color=8388640)
                        await ctx.message.channel.send(embed=embed_var)
                await react(1, ctx.message)
    return
    
@_set.command(aliases=['wm'])
async def setWelcomeMessage(ctx):
    if channel_guild == str(ctx.message.channel.id) or channel_guild == channel_bot:
        if ctx.message.author.guild_permissions.administrator:
            words_message_content = ctx.message.content.split()
            if len(words_message_content) > 2:
                new_wm_guild = ctx.message.content[8:len(ctx.message.content)]
                print(new_wm_guild)
                updateDB(new_wm = new_wm_guild)
                embed_var = discord.Embed(description='Message Set', color=8388640)
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

def updateDB(flag = 1, new_guild = id_guild, new_prefix = prefix_guild, new_channel = channel_guild, new_wc = wc_guild, new_wm = wm_guild):
    global id_guild, prefix_guild, channel_guild, wc_guild, wm_guild
    
    if new_guild is None:
        new_guild = id_guild
    if new_prefix is None:
        new_prefix = prefix_guild
    if new_channel is None:
        new_channel  = channel_guild
    if new_wc is None:
        new_wc = wc_guild
    if new_wm is None:
        new_wm = wm_guild
        
    if flag == 0:
        dict_db_guild.update({ new_guild: { 'prefix': prefix_bot, 'channel': channel_bot, 'welcome channel': wc_bot, 'welcome message': wm_bot}})
        writeDB(dict_db_guild)
    elif flag == 1:
        dict_db_guild.update({ new_guild: { 'prefix': new_prefix, 'channel': new_channel, 'welcome channel': new_wc, 'welcome message': new_wm }})
        writeDB(dict_db_guild)
    id_guild = new_guild
    prefix_guild = dict_db_guild[id_guild]["prefix"]
    channel_guild = dict_db_guild[id_guild]["channel"]
    wc_guild = dict_db_guild[id_guild]["welcome channel"]
    wm_guild= dict_db_guild[id_guild]["welcome message"]
    return

# --- main ---
client.loop.create_task(scoutReport(client))
client.run(token)
