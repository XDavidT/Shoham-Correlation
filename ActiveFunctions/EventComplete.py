from ActiveFunctions.Headers import Load_Events

def SuccessEvent(client, log_document,setting):
    events = Load_Events(setting)
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]
    success_collection = client[setting['policy-db-name']][setting['success-alert-collection-name']]
    success_collection.insert_one(log_document)
    semi_collection.delete_one(log_document)
    print(events[log_document['event']]['name'] + " alerted !!")
    print("done success")