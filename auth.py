import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def gmail_authenticate(client_secret_path='client_secret.json', token_path='token.pickle'):
    """
    Desktop OAuth flow. Expects client_secret.json (Desktop App) present.
    Returns (creds, gmail_service)
    """
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if not os.path.exists(client_secret_path):
            raise FileNotFoundError(f"{client_secret_path} not found.")
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as f:
            pickle.dump(creds, f)

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
    print("DEBUG: Gmail authentication successful")
    return creds, service
