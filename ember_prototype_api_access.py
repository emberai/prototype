from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import argparse

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Ember Prototype Google Calendar API Access'


def get_credentials(user):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.realpath('.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'account-credentials-' + user + '.json')

    store = oauth2client.file.Storage(credential_path)  # stores the users credentials --> TODO: put in database?
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

        print('Storing credentials to ' + credential_path)
    return credentials


def get_freebusy_query(user):
    """Gets the freebusy data from a calendar between now and 24 hours from now.

    Returns:
        A json that contains all of the times in which the user is busy.
    """
    credentials = get_credentials(user)
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    twenty_four_hours = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'

    request_query = {
        "timeMin": now,
        "timeMax": twenty_four_hours,
        # "timeZone": string, <-- optional, current default is UTC
        # "groupExpansionMax": 2,
        # "calendarExpansionMax": 2,
        "items": [
            {
                "id": "primary"
            }
        ]
    }

    # POST request to get freebusy data between now and 24 hours from now
    request = service.freebusy().query(body=request_query)
    freebusy_query = request.execute()
    return freebusy_query

# creates two separate jsons in the working directory that contain freebusy data
with open('data1.json', 'w') as json_file1:
    json.dump(get_freebusy_query('1'), json_file1)
with open('data2.json', 'w') as json_file2:
    json.dump(get_freebusy_query('2'), json_file2)
