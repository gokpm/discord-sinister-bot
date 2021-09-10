import json
from logging import error

prefix_db_fp = 'server_prefix_db.json'

def writeDB(file_dump):
    try:
        with open(prefix_db_fp, 'w') as prefix_db:
            json.dump(file_dump, prefix_db, indent = 4)
    except error:
        print(error)

def readDB():
    prefix_dict = None
    try:
        with open(prefix_db_fp, 'r') as prefix_db:
            prefix_dict = json.load(prefix_db)
    except error:
        print(error)
    
    return prefix_dict