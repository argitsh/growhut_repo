# analysis.py
import re
from collections import Counter
from datetime import datetime

def count_by_sender(messages):
    c = Counter()
    for m in messages:
        frm = m.get('from', 'unknown')
        c[frm] += 1
    return dict(c)

_money_re = re.compile(r'₹?\$?\s?([0-9]+(?:[.,][0-9]{2})?)')

def extract_amounts_from_text(text):
    out = []
    for m in _money_re.findall(text or ""):
        try:
            val = float(m.replace(',', ''))
            out.append(val)
        except:
            continue
    return out

def sum_expenses(messages):
    total = 0.0
    found = []
    for m in messages:
        body = m.get('snippet', '') or ""
        for amt in extract_amounts_from_text(body):
            total += amt
            found.append(amt)
    return total, found
