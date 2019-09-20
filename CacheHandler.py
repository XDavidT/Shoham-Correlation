from MongoHandler import Mongo_Connection
import json


# Get rules/events from file to variable
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
def Load_Rules(setting):
    Sync_Rules(setting)
    with open('cache/rules.json') as rules_file:
        rules = json.load(rules_file)
    return rules
def Load_Events(setting):
    Sync_Events(setting)
    with open('cache/events.json') as events_file:
        events = json.load(events_file)
    return events

# Write to local cache the rules & events
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
def Sync_Rules(setting):
    try:
        client = Mongo_Connection()
        rules_collection = client[setting['policy-db-name']][setting['rules-collection-name']]
        with open('cache/rules.json', 'w') as rules_cache:
            rules_cache.write('[')
            number_of_rules = rules_collection.count()          # getting the count of rules
            for i,rule in enumerate(rules_collection.find(),1): # to know who's the last one
                rules_cache.write(json.dumps(rule))             # in that case we can finish without
                if i !=number_of_rules:                         # extra comma (',')
                    rules_cache.write(',')
            rules_cache.write(']')
    except Exception as e:
        print(e)

def Sync_Events(setting):
    try:
        client = Mongo_Connection()
        events_collection = client[setting['policy-db-name']][setting['events-collection-name']]
        with open('cache/events.json', 'w') as events_cache:
            events_cache.write('[')
            number_of_rules = events_collection.count()          # getting the count of rules
            for i,rule in enumerate(events_collection.find(),1): # to know who's the last one
                events_cache.write(json.dumps(rule))             # in that case we can finish without
                if i !=number_of_rules:                          # extra comma (',')
                    events_cache.write(',')
            events_cache.write(']')
    except Exception as e:
        print (e)

# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
