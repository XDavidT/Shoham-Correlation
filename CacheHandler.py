from MongoHandler import Mongo_Connection
import json, os


# Load functions [Setting] #
def load_base_setting():
    with open('setting/base-setting.json') as config_file:
        setting = json.load(config_file)
    return setting


def load_setting():
    name = 'basic-setting' # Also in sync - static
    with open('setting/'+name+'.json') as setting_file:
        setting = json.load(setting_file)
    return setting


def load_alert_setting():
    name = 'alert-setting' # Also in sync - static
    with open('setting/'+name+'.json') as config_file:
        setting = json.load(config_file)
    return setting

# Get rules/events from file to variable
# Load functions [Rules/Events] #
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


def load_rules():
    check_cache_dir()
    with open('cache/rules.json') as rules_file:
        rules = json.load(rules_file)
    return rules


def load_events():
    check_cache_dir()
    with open('cache/events.json') as events_file:
        events = json.load(events_file)
    return events

# Write to local cache the rules & events
# Sync functions #
# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


def sync_rules():
    b_setting = load_base_setting()
    try:
        client = Mongo_Connection()
        rules_collection = client[b_setting['policy-db-name']][b_setting['rules-collection-name']]
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


def sync_events():
    b_setting = load_base_setting()
    try:
        client = Mongo_Connection()
        events_collection = client[b_setting['policy-db-name']][b_setting['events-collection-name']]
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


def sync_setting(what_setting):
    b_setting = load_base_setting()
    try:
        client = Mongo_Connection()
        setting_collection = client[b_setting['system-mgm-db-name']][b_setting['setting-collection-name']]
        setting = setting_collection.find_one({'_id': what_setting})

        with open('setting/'+what_setting+'.json','w') as setting_file:
            setting_file.write(json.dumps(setting))

    except Exception as e:
        print(e)

# - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #


def check_cache_dir():
    if not os.path.isdir('./cache'):
        os.mkdir('cache')


def main_sync():
    sync_rules()
    sync_events()

    settings = ['alert-setting', 'basic-setting']
    for i in settings:
        sync_setting(i)