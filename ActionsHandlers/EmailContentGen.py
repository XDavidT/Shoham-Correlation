from yattag import Doc
from CacheHandler import load_events

def HTML_Template(log_document):
    events = load_events()
    doc, tag, text = Doc().tagtext()

    try:
        with tag('div', dir='ltr'):
            with tag('div',align='center'):
                with tag('h1'):
                    text('! Important Alert from Shoham SIEM System !')
                    doc.stag('br')
            with tag('div', align='left'):
                with tag('h3'):
                    text('Report details:')
                    doc.stag('br')

                with tag('b'):
                    text('Event name: ')
                text(events[log_document['event']]['name'])
                doc.stag('br')

                with tag('b'):
                    text('Description: ')
                text(events[log_document['event']]['description'])
                doc.stag('br')

                with tag('b'):
                    text('Type: ')
                text(log_document['type'])
                doc.stag('br')

                with tag('b'):
                    text('Alerted time: ')
                text(str(log_document['offense_close_time']))
                doc.stag('br')

                with tag('b'):
                    text('Devices included: ')
                    doc.stag('br')
                with tag('ul'):
                    for device in log_document['device']:
                        with tag('li'):
                            text(device)

        return doc.getvalue()
    except Exception as e:
        print("Exception in HTML: " + str(e))
