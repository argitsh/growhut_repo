# Gmail Agent AI

## Project Overview
Gmail Agent AI is a Python-based intelligent assistant designed to interact with your Gmail account. It can search emails based on natural language instructions, analyze the results, and summarize them using OpenAI’s GPT-4o-mini model. The agent provides detailed information about sender, date, and subject for each email, making it ideal for managing assessments, interview notifications, and other important emails.

## Project Objectives
- Enable natural language querying of Gmail emails.
- Summarize emails clearly with sender, date, and subject.
- Group emails by sender for easy analysis.
- Integrate OpenAI LLM (GPT-4o-mini) for query generation and result summarization.
- Support simple analytics like counting emails or summarizing expenses.

## Installation Instructions
1. Clone the repository:
git clone https://github.com/your-username/gmail-agent-ai.git
cd gmail-agent-ai

2. Install required Python packages:
pip install -r requirements.txt

3.Setup and Configuration Guide

Gmail API Setup:

Go to Google Cloud Console
 and create a project.

Enable the Gmail API.

Create OAuth 2.0 Desktop credentials.

Download the client_secret.json file and place it in the project folder.

Environment Variables:

Create a .env file in the project folder.

Add your OpenAI API key:

OPENAI_API_KEY=your_openai_key_here


Important: Do not commit .env to public repositories.

Running the Project:

Run the main script:

python main.py


Follow the interactive prompts to enter instructions like:

“Find all assessment emails”

“Check for updates from Growhut Technologies via LinkedIn”

Gmail OAuth Flow:

The first time you run the project, a browser window will open to authenticate your Gmail account.

After authentication, a token.pickle file will be created to store credentials securely for future runs.

Example of queries and answers : 

#Q1do i ahve any emails from zaidi

Answer:
 You have received 5 emails from Zaidi, Abiha - Ext at Deloitte. Here are the details:

### From: Zaidi, Abiha - Ext <abizaidi.ext@deloitte.com>

1. **Date:** Fri, 26 Sep 2025
   **Subject:** Data Scientist/Gen-Ai Engineer - Online Assessment Drive - Deloitte India ||Consultant

2. **Date:** Fri, 26 Sep 2025
   **Subject:** Deloitte: Let`s Connect ||Opportunity in Data Science/ Generative AI/ Agentic AI

3. **Date:** Sun, 24 Aug 2025
   **Subject:** Thank you for your interest

4. **Date:** Fri, 8 Aug 2025
   **Subject:** Data Scientist/Gen-Ai Engineer - Online Assessment Drive - Deloitte India ||Consultant

5. **Date:** Fri, 8 Aug 2025
   **Subject:** Deloitte: Let`s Connect ||Opportunity in Data Scientist - Gen AI Role||

If you need further details about any specific email, feel free to ask!

#Q2 what mesage i ahve from zomato in last 2 days

Answer:
 Here are the messages you received from Zomato in the last 2 days:

### Sender: Zomato <noreply@mailers.zomato.com>
1. **Date:** Tue, 30 Sep 2025
   **Subject:** He's got the upper hand 💪

2. **Date:** Sun, 28 Sep 2025
   **Subject:** Bumrah knows a cheat code 🙌

### Sender: Zomato <noreply@zomato.com>
1. **Date:** Fri, 26 Sep 2025
   **Subject:** Login Alert for your Zomato account!

These are the most recent emails from Zomato within the specified timeframe.
#Q3  did i respond to aarti sharma

Answer:
 You have not responded to Aarti Sharma, as there are no emails from her in your Gmail account.
 
 #Q4 mesaage from brim labs in last 5 days

Answer:
 Here are the emails from Brim Labs received in the last 5 days:

### Sender: Brim Labs via LinkedIn <newsletters-noreply@linkedin.com>

1. **Date:** Mon, 29 Sep 2025
   **Subject:** From Data Chaos to AI Agent: How Startups Can Unlock Hidden Value in 8 Weeks

2. **Date:** Fri, 26 Sep 2025
   **Subject:** How to Hire AI-Native Teams Without Scaling Your Burn Rate

3. **Date:** Wed, 24 Sep 2025
   **Subject:** Co-Building vs Outsourcing: Why Founders Need Tech Partners Who Act Like Co-Founders

These are the three most recent emails from Brim Labs within the specified timeframe. If you need further details or additional emails, please let me know!

#Q5 did i recieve any email on 30 september related to assessments or interviews

Answer:
 On September 30, 2023, you received one email related to assessments or interviews. Here are the details:

### Sender: service@naukri.com
- **Date:** September 30, 2023, 10:47 AM IST
- **Subject:** Functional Area Insight Report Location wise from Naukri Fast-Forward!

This is the only email you received on that date.

# attaching link of video : https://drive.google.com/file/d/1dQheOLt-qbNPBwkiumtEPrQh1JwvxI1h/view?usp=drive_link
