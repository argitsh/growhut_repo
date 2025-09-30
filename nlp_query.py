
# nlp_query.py
import re
from datetime import datetime

def parse_query_to_gmail(text: str):
    """
    Convert natural language to Gmail search query.
    Handles 'latest', 'interview', 'about topic', 'month year'.
    """
    q_parts = []
    text_lower = text.lower()

    latest = "latest" in text_lower or "most recent" in text_lower
    max_results = 1 if latest else 50

    m = re.search(r'from (\S+@\S+)', text_lower)
    if m:
        q_parts.append(f"from:{m.group(1)}")

    if "interview" in text_lower:
        q_parts.append('(subject:interview OR interview)')

    m = re.search(r'about ([\w\s]+?)(?: in | from | between |$)', text_lower)
    if m:
        topic = m.group(1).strip()
        q_parts.append(f'(subject:{topic} OR "{topic}")')

    m = re.search(r'(\w+)\s+(\d{4})', text)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%B")
        except:
            try:
                dt = datetime.strptime(m.group(1), "%b")
            except:
                dt = None
        if dt:
            year = int(m.group(2))
            after = f"{year}/{dt.month:02d}/01"
            before = f"{year}/{dt.month:02d}/31"
            q_parts.append(f"after:{after} before:{before}")

    query = ' '.join(q_parts) if q_parts else text
    return query, max_results
