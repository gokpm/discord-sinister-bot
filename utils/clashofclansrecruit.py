import asyncpraw
import json
import os
from utils.readWriteDB import *
import discord
import asyncio

async def cache(file_open_mode):
    fp_cache_reddit = r'cache_reddit.json'
    global archive
    if file_open_mode == 'r':
        with open(fp_cache_reddit, 'r') as cache_reddit:
            archive = json.load(cache_reddit)
    elif file_open_mode == 'r+':
        archive.append(post.id)
        with open(fp_cache_reddit, 'r+') as cache_reddit:
                json.dump(archive, cache_reddit, indent = 4)
    return

async def redditLogin():
    await cache('r')
    global list_post
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
                await cache('r+')
                if '[searching]' in post_content:
                    embed_var = discord.Embed(title=post.title, description=post.selftext, color=8388640, url = post.url)
                    for i_guild in dict_db_guild:
                        i_channel = dict_db_guild[i_guild]['channel']
                        if i_channel != 'any':
                            channel = client.get_channel(int(i_channel))
                            await channel.send(embed=embed_var)
        await asyncio.sleep(60)
    return

                                
                                    
                        
                    
                    
                

                
    




