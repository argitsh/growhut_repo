import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
import email_client as ec
import analysis

# Load .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- LLM-driven Gmail query generator ----
def instruction_to_gmail_query(instruction: str) -> str:
    """
    Converts any natural language instruction into a Gmail search query.
    Uses Gmail search operators like subject:, from:, after:, has:attachment.
    """
    prompt = f"""
Convert this instruction into a Gmail search query string.
Instruction: "{instruction}"
Use Gmail search operators like subject:, from:, after:, has:attachment.
Return only the query string, no explanation.
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Gmail search assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0
        )
        query = resp.choices[0].message.content.strip()
        return query
    except Exception as e:
        print("DEBUG: LLM query generation failed, using raw instruction as query:", e)
        return instruction  # fallback to literal instruction

# ---- PlannerAgent ----
def planner(instruction: str) -> List[Dict[str, Any]]:
    gmail_q = instruction_to_gmail_query(instruction)
    return [
        {"action": "search", "params": {"query": gmail_q, "max_results": 50}},
        {"action": "analyze", "params": {"analysis": "summary"}}
    ]

# ---- ExecutorAgent ----
def execute_plan(service, plan: List[Dict[str, Any]]):
    results = []
    last_search_msgs = []

    for step in plan:
        action = step.get('action')
        params = step.get('params', {})

        if action == 'search':
            q = params.get('query')
            maxr = params.get('max_results', 50)
            msgs = ec.search_messages(service, q, max_results=maxr)
            enriched = []
            for m in msgs:
                headers = ec.parse_headers(m)
                body = ec.extract_plain_text(m)
                enriched.append({
                    'id': m['id'],
                    'from': headers.get('From', 'Unknown Sender'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', 'No Date'),
                    'snippet': body[:150] if body else "",
                })
            last_search_msgs = enriched
            results.append({
                'action': 'search',
                'count': len(enriched),
                'emails': enriched  # pass full enriched emails
            })

            if maxr == 1 and enriched:
                results.append({'action': 'latest_email', 'email': enriched[0]})

        elif action == 'analyze':
            kind = params.get('analysis', 'summary')
            if kind == 'sum_expenses':
                total, found = analysis.sum_expenses(last_search_msgs)
                results.append({'action':'analyze','type':'sum_expenses','total': total, 'found': found})
            else:
                cnt = len(last_search_msgs)
                by_sender = analysis.count_by_sender(last_search_msgs)
                results.append({'action':'analyze','type':'summary','count':cnt,'by_sender':by_sender})

    return results

# ---- Coordinator ----
def run_agent(service, instruction: str, require_confirmation=True):
    plan = planner(instruction)
    res = execute_plan(service, plan)
    return {'status':'executed','plan': plan, 'result': res}

def summarize_result(instruction: str, results):
    """
    Use LLM to turn raw execution results into a natural language answer.
    Now includes sender, date, and subject for each email.
    """
    if not client.api_key:
        # Fallback: show basic info if LLM is unavailable
        summary_lines = []
        for step in results:
            if step.get('action') == 'search' and 'emails' in step:
                for e in step['emails']:
                    summary_lines.append(f"{e['from']} | {e['date']} | {e['subject']}")
        return "\n".join(summary_lines) if summary_lines else f"Results: {results}"

    # Construct prompt for LLM
    prompt = f"""
User asked: {instruction}

Here are the raw results from Gmail operations:
{json.dumps(results, indent=2, default=str)}

Please summarize the results into a clear, detailed answer.
For each email, include:
- Sender
- Date
- Subject

Group emails by sender, and list all emails individually under each sender.
If many emails exist, list at least the 3 most recent per sender.
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes Gmail query results clearly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Raw results (failed to summarize): {results} | Error: {e}"
