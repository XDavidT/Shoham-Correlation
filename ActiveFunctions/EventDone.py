from ActiveFunctions.Headers import Load_Events
from ActionsHandlers.EmailHandler import AlertOnEmail

def SuccessEvent(client, log_document,setting):
    events = Load_Events(setting)
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]
    success_collection = client[setting['policy-db-name']][setting['success-alert-collection-name']]
    success_collection.insert_one(log_document)
    semi_collection.delete_one(log_document)
    AlertOnEmail(log_document)

def FailEvent(client,log_document,setting):
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]
    fail_collection = client[setting['policy-db-name']][setting['fail-alert-collection-name']]
    fail_collection.insert_one(log_document)
    semi_collection.delete_one(log_document)