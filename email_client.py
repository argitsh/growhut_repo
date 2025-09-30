# email_client.py
import base64
from email.mime.text import MIMEText

def fetch_latest(service, n=10):
    res = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=n).execute()
    msgs = res.get('messages', [])
    out = []
    for m in msgs:
        full = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        out.append(full)
    return out

def search_messages(service, query, max_results=50):
    res = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    msgs = res.get('messages', [])
    out = []
    for m in msgs:
        full = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        out.append(full)
    return out

def parse_headers(message):
    headers = {}
    for h in message.get('payload', {}).get('headers', []):
        headers[h['name']] = h['value']
    return headers

def extract_plain_text(message):
    payload = message.get('payload', {})

    def _walk(parts):
        if not parts:
            return ""
        for p in parts:
            if 'parts' in p:
                txt = _walk(p['parts'])
                if txt:
                    return txt
            if p.get('mimeType') == 'text/plain' and p.get('body', {}).get('data'):
                data = p['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
        return ""
    if 'parts' in payload:
        return _walk(payload['parts'])
    else:
        body = payload.get('body', {}).get('data')
        return base64.urlsafe_b64decode(body).decode('utf-8', errors='replace') if body else ""
