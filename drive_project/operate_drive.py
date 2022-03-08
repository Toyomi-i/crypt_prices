from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
import os

def setting():
    SCOPES  = ['https://www.googleapis.com/auth/drive'] 
    store   = file.Storage('token.json')
    creds   = store.get()

    if not creds or creds.invalid:
        flow    = client.flow_from_clientsecrets('./client_secret.json', SCOPES)
        creds   = tools.run_flow(flow, store)
    
    drive_service \
            = build('drive', 'v3', http=creds.authorize(Http())) 
    return drive_service


def create_folder(drive_service, folder_name, id):
    "id: id of save folder"
    file_metadata = {
        'name':     folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':  id
    }

    file = drive_service.files().create(
        body    = file_metadata, 
        fields  = 'id'
    ).execute()  
    
    # str to confirm created folder id
    str = 'Created Folder ID: %s' % file.get('id')
    return str


def upload_to_drive(drive_service, file_name, local_file_path, id):
    file_metadata = {
        'name':     file_name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents':  [id]
    }
    media   = MediaFileUpload(
        local_file_path, 
        mimetype    = 'text/csv', 
        resumable   = True
    )
    file    = drive_service.files().create(
        body        = file_metadata, 
        media_body  = media, 
        fields      = 'id'
    ).execute()


def main():
    os.chdir('/Users/toyomiishida/Documents/personal/drive_project')
    drive_service = setting()

    # create folder to save prices file
    #str = create_folder(
    #    drive_service, 
    #    folder_name='prices_file', 
    #    id=['XXXXXXXX']
    #)
    #print(str)

    # upload prices file to goolge drive
    upload_to_drive(
            drive_service, 
            file_name       = '2022_02_atmprices',
            local_file_path = '../prices_file/2022_02_atmprices.csv',
            id              = 'XXXXXXXXXX'
        )


if __name__ == '__main__':
    main()