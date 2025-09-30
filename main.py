# main.py
import os
from auth import gmail_authenticate
from agent import run_agent, execute_plan, summarize_result
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def pretty_print_results(obj):
    print(json.dumps(obj, indent=2, default=str))

def main():
    print("Authenticating Gmail...")
    creds, service = gmail_authenticate()
    print("Authenticated.")

    while True:
        instr = input("\nEnter instruction (or 'exit'): ").strip()
        if not instr:
            continue
        if instr.lower() in ('exit','quit'):
            break

        res = run_agent(service, instr, require_confirmation=True)

        if res.get('status') == 'need_confirmation':
            print("Planned steps (review before execution):")
            pretty_print_results(res['plan'])
            ans = input("Approve plan? (yes/no): ").strip().lower()
            if ans.startswith('y'):
                exec_res = execute_plan(service, res['plan'])
                print("Execution result:")
                pretty_print_results(exec_res)
            else:
                print("Plan aborted.")
        else:
            answer = summarize_result(instr, res['result'])
            print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()
