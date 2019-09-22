import asyncio
from MongoHandler import Mongo_Connection
from CacheHandler import *

async def CheckSemi():
    client = Mongo_Connection()
    setting = Load_Setting()
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

    semi_alert_list_size = semi_collection.find({}).count()
    if(len(semi_alert_list_size) == 0): # Nothing waiting
        await asyncio.sleep(setting['time_to_semi'])
    else:   # Something wait..
        semi_collection.find({})
        for log in semi_collection.find({}):
            pass #TODO: still open
