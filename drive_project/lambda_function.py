from googleapiclient.discovery import build 
from googleapiclient.http import MediaFileUpload 
from oauth2client.service_account import ServiceAccountCredentials

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
ENDPOINT = "https://1suCarNUraHcF3FzvwPyyqbM-Cn32NMNf.appsync-api.ap-northeast-1.amazonaws.com/graphql"
API_KEY = "XXXXXXX"
_headers = {
    "Content-Type": "application/graphql",
    "x-api-key": API_KEY,
}
_transport = RequestsHTTPTransport(
    headers = _headers,
    url = ENDPOINT,
    use_json = True,
)
_client = Client(
    transport = _transport,
    fetch_schema_from_transport = True,
)


def uploadFileToGoogleDrive(fileName, localFilePath):
    try:
        ext = os.path.splitext(localFilePath.lower())[1][1:]
        if ext == "jpg":
            ext = "jpeg"
        mimeType = "image/" + ext

        service = getGoogleService()
        file_metadata = {"name": fileName, "mimeType": mimeType, "parents": ["*********************************"] } 
        media = MediaFileUpload(localFilePath, mimetype=mimeType, resumable=True) 
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    except Exception as e:
        logger.exception(e)

def getGoogleService():
    scope = ['https://www.googleapis.com/auth/drive.file'] 
    keyFile = 'service-account-key.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyFile, scopes=scope)

    return build("drive", "v3", credentials=credentials, cache_discovery=False) 