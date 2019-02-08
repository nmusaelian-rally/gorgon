import json
import re
import requests
from helpers.dbconn import update

BASE_RALLY_URL = 'https://rally1.rallydev.com/slm/webservice/v2.0'

def parseAndDump(consumer, producer, dbconnection):
    # iterate over consumer, pulling out payload items
    for message in consumer:
        md = json.loads(message.value.decode())
        # yank out the installation_id from the message dict (md)
        installation_id = md['payload']['installation']['id']
        # query for item in db, update the hit_count and last_used fields for installation_id
        # update(db, installation_id)
        api_key = update(dbconnection, installation_id)
        #dbconnection.commit()
        # yank out all the cruft from payload, reducing it to a dict of field/values suitable for create/update via Rally WSAPI
        pr_info = md['payload']['pull_request']
        actionable_items = _assembleRallyItems(pr_info, api_key)
        # dump the resulting payload chunk into the next topic via the producer
        for actionable_item in actionable_items:
            producer.produce(json.dumps(actionable_item).encode())

    # consumer.stop()  # we may have to do this as part of a graceful shutdown process (which we don't know how if works...)

def _assembleRallyItems(item_data, api_key):
    short_refs    = _getRallyArtifactUrls(item_data['body'])
    artifact_refs = _getRallyArtifactRefs(short_refs, api_key)
    items = []
    for art_ref in artifact_refs:
        rally_payload = {'ExternalID'          : item_data['id'],
                         'ExternalFormattedId' : item_data['number'],
                         'Name'                : item_data['title'],
                         'Artifact'            : art_ref['ref'],
                         'Url'                 : item_data['url']
                        }
        item = {'workspace'     : art_ref['workspace'],
                'project'       : art_ref['project'],
                'rally_payload' : rally_payload}
        items.append(item)
    return items

def _extractLinkFromBody(target):
    art_links = re.findall(r'(https://rally1.rallydev.com/#detail/(\w+/)?(\w+/\d+))', target, re.M)
    return art_links


def _getRallyArtifactUrls(target):
    # extract item type
    # extract objectid
    # https://rally1.rallydev.com/#detail/userstory/233499351572

    short_refs = []
    links = _extractLinkFromBody(target)
    for link in links:
        _, short_ref = link[0].split('/#detail/', 1)
        short_refs.append(short_ref.replace('?fdp=true',''))
    return short_refs

def _getRallyArtifactRefs(short_refs, api_key):
    art_refs = []
    for short_ref in short_refs:
        if 'userstory' in short_ref:
            short_ref = short_ref.replace('userstory', 'hierarchicalrequirement')

        wi_type = re.sub(r'/\d+$', '', short_ref)
        wi_type = wi_type.replace('portfolioitem/', '')

        full_url = "%s/%s" % (BASE_RALLY_URL, short_ref)
        headers  = {'zsessionid':api_key}
        r = requests.get(full_url, headers=headers)
        if r.status_code == 200:
            rally_response = json.loads(r.text)
            big_key = list(rally_response.keys())[0]
            rally_response[big_key.lower()] = rally_response[big_key]  # "dupe" a slot with the lower case translation of the big_key
            if wi_type in rally_response:
                # art_refs.append(short_ref)
                workspace = rally_response[wi_type]['Workspace']['_ref']
                project   = rally_response[wi_type]['Project'  ]['_ref']
                art_refs.append({'ref'      : short_ref,
                                 'workspace': workspace,
                                 'project'  : project})

    return art_refs










