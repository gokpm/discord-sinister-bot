import json
import os
from logging import error

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
            with open(fp_cache_reddit, 'w') as cache_reddit:
                json.dump([], cache_reddit, indent = 4)
    except error:
        print(error)
