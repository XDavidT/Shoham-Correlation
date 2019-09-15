import datetime
from MongoHandler import *

def LogsTracker(setting):
    client = Mongo_Connection()
    logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours'])

    for log in logs_collection.find(
            {'insert_time': {'$gte': last_time_delta}}):  # List is already from old time to last
        print(log)

def Load_Rules():
    with open('cache/rules.json') as rules_file:
        rules = json.load(rules_file)
    return rules

def Save_Rules(rules):
    with open('cache/rules.json','w+') as rules_file:
        rules_dump = json.dump(rules)
        rules_file.write(rules_dump)
        rules_file.close()

def Rule_Translate(setting,rules,rule_id):
    try:    #If we found it in cache
        return rules[rule_id]
    except:
        client = Mongo_Connection()
        rules_collection = client[setting['policy-db-name']][setting['rules-collection-name"']]
        rules[rule_id] = rules_collection.find_one({"_id":rule_id})
        Save_Rules(rules) #Save the new rule to cache
        return rules[rule_id]