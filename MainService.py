import datetime
from pymongo import MongoClient

last_time_detla = datetime.datetime.now() - datetime.timedelta(hours = 2)
client = MongoClient('mongodb://13.68.170.154:27017/')

logs_collection = client['clientManager']['clientLog'] # Select DB

with open('test.txt','a') as output:
    for log in logs_collection.find({'insert_time' : {'$gte' : last_time_detla} }):
        output.write(str(log))