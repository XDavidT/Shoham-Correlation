from CacheHandler import load_events
from ActionsHandlers.EmailHandler import AlertOnEmail

def SuccessEvent(client, log_document,b_setting):
    events = load_events(b_setting)
    semi_collection = client[b_setting['policy-db-name']][b_setting['semi-alert-collection-name']]
    success_collection = client[b_setting['policy-db-name']][b_setting['success-alert-collection-name']]
    success_collection.insert_one(log_document)
    semi_collection.delete_one(log_document)
    AlertOnEmail(log_document)

def FailEvent(client,log_document,b_setting):
    semi_collection = client[b_setting['policy-db-name']][b_setting['semi-alert-collection-name']]
    fail_collection = client[b_setting['policy-db-name']][b_setting['fail-alert-collection-name']]
    fail_collection.insert_one(log_document)
    semi_collection.delete_one(log_document)