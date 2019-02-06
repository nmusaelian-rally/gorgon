import json
from helpers.dbconn import update


def parseAndDump(consumer, producer, db):
    # iterate over consumer, pulling out payload items
    for message in consumer:
        md = json.loads(message.value.decode())
        # yank out the installation_id from the message dict (md)
        installation_id = md['payload']['installation']['id']
        # query for item in db, update the hit_count and last_used fields for installation_id
        update(db, installation_id)
        # yank out all the cruft from payload, reducing it to a dict of field/values suitable for create/update via Rally WSAPI
        if 'action' in md['payload']:
           if 'action' == 'open':
               body = md['payload']['pull_request']['body']
               # rally_url = parseForRallyRef(body)
           elif 'action' == 'closed':
               body = md['payload']['pull_request']['body']
           #elif 'action' == 'synchronized':

        actionable_item = _assembleRallyItem('PullRequest', md['payload']['pull_request'])
        # dump the resulting payload chunk into the next topic via the producer
        producer.produce(actionable_item.encode())

    # consumer.stop()  # we may have to do this as part of a graceful shutdown process (which we don't know how if works...)

def _assembleRallyItem(item_type, item_data):
    artifact = _getRallyArtifactUrl(item_data['body'])
    actionable_data = {'ExternalID'          : item_data['id'],
                       'ExternalFormattedId' : item_data['number'],
                       'Name'                : item_data['title'],
                       'Artifact'            : artifact,
                       'Url'                 : item_data['url']
                      }
    return actionable_data

def _getRallyArtifactUrl(target):
    # extract item type
    # extract objectid
    base_url = 'https://rally1.rallydev.com/slm/webservice/v2.0'
    full_url = "%s/%s/%s" % (base_url, item_type, oid)
    return None










