# AI Bulk Email Agent

**Live App:** [https://ai-email-agent-xtv0.onrender.com](https://ai-email-agent-xtv0.onrender.com)

## Technical Overview
This is a full-stack SaaS application for generating and dispatching personalized cold emails at scale using AI. 
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Background Workers:** Celery & Redis (Upstash)
- **AI Integration:** LangGraph + Groq API 
- **Deployment:** Render (Monolithic container running FastAPI, Celery, and Streamlit simultaneously)

---

## How to Use the App

### 1. Configuration
When you open the app, you will see an **App Settings** sidebar on the left. You must provide your own credentials:
- **Groq API Key**: Get a free API key from the [Groq Console](https://console.groq.com).
- **SMTP Email**: The email address you want to send from (e.g., your Gmail).
- **SMTP App Password**: An app-specific password (if using Gmail, generate this in your Google Account Security settings).

### 2. Upload Data
- Under Step 1, upload a `.csv` or `.xlsx` file containing your recipient list.
- The app will automatically detect columns like `Name`, `Email`, etc., and show a preview of your data.

### 3. Launch Campaign
- Enter a **Campaign Name**.
- Provide **AI Prompt Instructions** (e.g., *"Write a friendly email introducing our new product features, keep it under 3 paragraphs"*).
- Click **Launch Campaign**. The AI will generate highly personalized email drafts for every recipient in the background.

### 4. Review & Send
- Scroll down to Step 3 and click **Refresh Drafts** to see the AI's work.
- You can manually **Edit** any draft if you want to tweak it.
- Once satisfied, click **Approve & Save**.
- Finally, click **Send Email Now**. The app will dispatch the email directly to the recipient's inbox using your configured SMTP credentials!
