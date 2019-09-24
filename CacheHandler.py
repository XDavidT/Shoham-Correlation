from MongoHandler import Mongo_Connection
import json, os


def Load_Setting():
    with open('setting/setting.json') as config_file:
        setting = json.load(config_file)
    return setting

# Get rules/events from file to variable
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
def Load_Rules(setting):
    Check_Cache_Dir()
    Sync_Rules(setting)
    with open('cache/rules.json') as rules_file:
        rules = json.load(rules_file)
    return rules
def Load_Events(setting):
    Check_Cache_Dir()
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
            rules_cache.write('{')
            number_of_rules = rules_collection.count()          # getting the count of rules
            for i,rule in enumerate(rules_collection.find(),1): # to know who's the last one
                rules_cache.write('"'+rule['_id']+'":')         # Adding ID before the rule to find it in O(1)
                rules_cache.write(json.dumps(rule))             # Paste the rule
                if i !=number_of_rules:                         # Check for last one ( need ignore last comma )
                    rules_cache.write(',')
            rules_cache.write('}')
        client.close()
    except Exception as e:
        print(e)


def Sync_Events(setting):
    try:
        client = Mongo_Connection()
        events_collection = client[setting['policy-db-name']][setting['events-collection-name']]
        with open('cache/events.json', 'w') as events_cache:
            events_cache.write('{')
            number_of_events = events_collection.count()          # getting the count of rules
            for i,event in enumerate(events_collection.find(),1): # to know who's the last one
                events_cache.write('"' + event['_id'] + '":')
                events_cache.write(json.dumps(event))             # in that case we can finish without
                if i !=number_of_events:                          # extra comma (',')
                    events_cache.write(',')
            events_cache.write('}')
        client.close()
    except Exception as e:
        print (e)


# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #
def Check_Cache_Dir():
    if not os.path.isdir('./cache'):
        os.mkdir('cache')