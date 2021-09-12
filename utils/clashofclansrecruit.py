import asyncpraw
import json
import os
from utils.readWrite import *
import discord
import asyncio

async def redditLogin():
    global archive
    global list_post
    archive = readRedditCache()
    reddit = asyncpraw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT'])
    reddit.read_only = True
    sub = await reddit.subreddit('clashofclansrecruit')
    list_post = [submission async for submission in sub.new(limit = 250)]
    list_post.reverse()
    return

async def scoutReport(client):
    global post
    await client.wait_until_ready()
    await redditLogin()
    while True:
        dict_db_guild = readDB()
        for post in list_post:
            if not post.id in archive:
                post_content = post.title + ' ' + post.selftext
                post_content = post_content.lower().split()
                archive.append(post.id)
                writeRedditCache(archive)
                if '[searching]' in post_content:
                    embed_var = discord.Embed(title=post.title, description=post.selftext, color=8388640, url = post.url)
                    for i_guild in dict_db_guild:
                        i_channel = dict_db_guild[i_guild]['channel']
                        if i_channel != 'any':
                            channel = client.get_channel(int(i_channel))
                            await channel.send(embed=embed_var)
        await asyncio.sleep(60)
    return

                                
                                    
                        
                    
                    
                

                
    




