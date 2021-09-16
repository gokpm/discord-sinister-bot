import asyncpraw
import json
import os
from utils.readWrite import *
import discord
import asyncio

async def redditLogin():
    global latest_post_time
    global list_post
    latest_post_time = readRedditCache()
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
    global post, latest_post_time
    await client.wait_until_ready()
    await redditLogin()
    while True:
        dict_db_guild = readDB()
        for post in list_post:
            if post.created_utc > latest_post_time:
                post_content = post.title + ' ' + post.selftext
                post_content = post_content.lower().split()
                if '[searching]' in post_content:
                    latest_post_time = post.created_utc
                    writeRedditCache(latest_post_time)
                    embed_var = discord.Embed(title=post.title, description=post.selftext, color=8388640, url = post.url)
                    for i_guild in dict_db_guild:
                        convert_guild = client.get_guild(int(i_guild))
                        i_channel = dict_db_guild[i_guild]['reddit channel']
                        i = 0
                        if i_channel != 'N/A':
                            for j_channel in convert_guild.channels:
                                if str(j_channel.id) == i_channel:
                                    i += 1
                            if i > 1:
                                channel = client.get_channel(int(i_channel))
                                await channel.send(embed=embed_var)
        await asyncio.sleep(60)
    return

                                
                                    
                        
                    
                    
                

                
    




