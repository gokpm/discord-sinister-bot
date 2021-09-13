import json
import os
from logging import error
import time

fp_db_guild = r'db_guild.json'
fp_cache_reddit = r'cache_reddit.json'

def writeDB(dict_to_dump):
    try:
        with open(fp_db_guild, 'w') as db_guild:
            json.dump(dict_to_dump, db_guild, indent = 4)
    except error:
        print(error)

def readDB():
    dict_db_guild = None
    try:
        with open(fp_db_guild, 'r') as db_guild:
            dict_db_guild = json.load(db_guild)
    except error:
        print(error)
    return dict_db_guild

def checkAndCreateDB():
    try:
        if (not os.path.isfile(fp_db_guild)):
            writeDB({})
        if (not os.path.isfile(fp_cache_reddit)):
            writeRedditCache(time.time() - 24*60*60)
    except error:
        print(error)
    return

def readRedditCache():
    with open(fp_cache_reddit, 'r') as cache_reddit:
        data_read = json.load(cache_reddit)
    return data_read

def writeRedditCache(data_to_dump):
    with open(fp_cache_reddit, 'w') as cache_reddit:
        json.dump(data_to_dump, cache_reddit, indent = 4)
    return
