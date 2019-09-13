import datetime
from pymongo import MongoClient

start = datetime.datetime.now() - datetime.timedelta(hours = 2)
end = datetime.datetime.now()
client = MongoClient('mongodb://13.68.170.154:27017/')

logs_collection = client['clientManager']['clientLog'] # Select DB
print(start)

with open('test.txt','a') as output:
    for log in logs_collection.find({'insert_time' : {'$gte' : start} }):
        output.write(str(log))