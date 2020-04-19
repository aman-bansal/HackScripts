from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors

SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.metadata']


def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    return service


def get_unread_updates_emails(service):
    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds=['UNREAD', 'INBOX', 'CATEGORY_UPDATES']).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', labelIds=['UNREAD', 'INBOX','CATEGORY_UPDATES'],
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s', error)


def get_unread_forum_emails(service):
    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds=['UNREAD', 'INBOX', 'CATEGORY_FORUMS']).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', labelIds=['UNREAD', 'INBOX', 'CATEGORY_FORUMS'],
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s', error)


def get_unread_personal_emails(service):
    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds=['UNREAD', 'INBOX', 'CATEGORY_PERSONAL']).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me',
                                                       labelIds=['UNREAD', 'INBOX', 'CATEGORY_PERSONAL'],
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s', error)


def get_unread_important_emails(service):
    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds=['UNREAD', 'INBOX', 'IMPORTANT']).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me',
                                                       labelIds=['UNREAD', 'INBOX', 'IMPORTANT'],
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s', error)


def mark_email_read(service, messages):
    for message in messages:
        try:
            service.users().messages().modify(userId='me', id=message['id'], body=create_message_labels()).execute()
        except errors.HttpError as error:
            print('An error occurred: %s', error)


def create_message_labels():
    return {'removeLabelIds': ['UNREAD']}


if __name__ == '__main__':
    service = authenticate()
    messages = get_unread_forum_emails(service=service)
    print("forum email count", messages.__len__())
    mark_email_read(service=service, messages=messages)

    messages = get_unread_updates_emails(service=service)
    print("updates email count", messages.__len__())
    mark_email_read(service=service, messages=messages)

    messages = get_unread_personal_emails(service=service)
    print("personal email count", messages.__len__())
    mark_email_read(service=service, messages=messages)

    messages = get_unread_important_emails(service=service)
    print("important email count", messages.__len__())
    mark_email_read(service=service, messages=messages)
