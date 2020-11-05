#!/usr/bin/python

# Retrieve the authenticated user's uploaded videos.
# Sample usage:
# python my_uploads.py

import argparse
import os
import re

for i in range(3):
  try:
    import google.oauth2.credentials
    import google_auth_oauthlib.flow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google_auth_oauthlib.flow import InstalledAppFlow
    break
  
  except:
    os.system('pip install --upgrade google-api-python-client')

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.channel-memberships.creator']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_my_members_list():
  # Retrieve the contentDetails part of the channel resource for the
  # authenticated user's channel.
  channels_response = youtube.members().list(
    part='contentDetails'
  ).execute()

  for channel in channels_response['items']:
    # From the API response, extract the playlist ID that identifies the list
    # of videos uploaded to the authenticated user's channel.
    return channel['contentDetails']['relatedPlaylists']['uploads']

  return None

if __name__ == '__main__':
  youtube = get_authenticated_service()

  try:
    
    print(get_my_members_list())

  except HttpError as e:
    print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')
