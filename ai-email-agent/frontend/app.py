import streamlit as st
import requests
import pandas as pd

# The URL where our FastAPI backend is running
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Email Agent", layout="wide")

st.markdown('''
<style>
    /* Make inputs pop with very light cream backgrounds and soft borders */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1px solid #BAB2B5 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        color: #123C69 !important;
    }
    
    /* Make buttons smooth and distinct (Dark Magenta) */
    .stButton > button {
        background-color: #AC3B61 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #8A2E4C !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Style the table for a cleaner look */
    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Make alerts softer */
    .stAlert {
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        border: 1px solid #BAB2B5 !important;
    }
</style>
''', unsafe_allow_html=True)

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("AI Bulk Email Agent")
    st.markdown("Upload your recipient data (CSV or Excel) and provide a custom prompt to generate personalized emails.")

with header_col2:
    # A simple, creative aesthetic design using overlapping geometric circles with the palette colors
    st.markdown('''
        <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:20px;">
            <div style="position:relative; width:120px; height:120px;">
                <div style="position:absolute; top:10px; right:40px; width:70px; height:70px; border-radius:50%; background-color:#AC3B61; opacity:0.85;"></div>
                <div style="position:absolute; top:40px; right:10px; width:50px; height:50px; border-radius:50%; background-color:#123C69; opacity:0.9;"></div>
                <div style="position:absolute; top:60px; right:60px; width:40px; height:40px; border-radius:50%; background-color:#EDC7B7; opacity:0.95;"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
st.divider()

# Sidebar for Configuration
st.sidebar.header("App Settings")
st.sidebar.markdown("Configure your keys to use the app.")
groq_key = st.sidebar.text_input("Groq API Key", type="password")
smtp_email = st.sidebar.text_input("SMTP Email (e.g., Gmail)", placeholder="your.email@gmail.com")
smtp_password = st.sidebar.text_input("SMTP App Password", type="password")

# Section 1: File Upload & Data Inspection
st.header("Step 1: Upload Recipient Data")

uploaded_file = st.file_uploader(
    "Choose a CSV or XLSX file", 
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    st.info(f"File selected: `{uploaded_file.name}`. Sending to FastAPI backend for parsing...")

    # Send the uploaded file as multipart/form-data to FastAPI
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/parse-file", files=files)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Successfully parsed **{result['filename']}**! Found **{result['total_rows']}** rows.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Recipients", result["total_rows"])
            with col2:
                st.write("**Detected Columns:**", ", ".join([f"`{c}`" for c in result["columns"]]))
            
            st.subheader("Data Preview (First 5 Rows)")
            preview_df = pd.DataFrame(result["preview"])
            st.dataframe(preview_df, width="stretch")
            
            # Store parsed data in Streamlit Session State for the next steps
            st.session_state["recipient_data"] = result["records"]
            st.session_state["columns"] = result["columns"]
            
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to FastAPI server at port 8000. Is Uvicorn running?")

# Section 2: Campaign Setup (Only shows up if file is successfully parsed)
if "recipient_data" in st.session_state and len(st.session_state["recipient_data"]) > 0:
    st.divider()
    st.header("Step 2: Configure & Launch Campaign")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        campaign_name = st.text_input("Campaign Name", placeholder="e.g., Q3 Product Update")
    
    with col2:
        prompt_template = st.text_area(
            "AI Prompt Instructions", 
            placeholder="Write a friendly email introducing our new features. Mention their role and company if available.",
            height=100
        )
        
    if st.button("Launch Campaign", type="primary"):
        if not campaign_name or not prompt_template:
            st.warning("Please provide both a Campaign Name and an AI Prompt.")
        elif not groq_key:
            st.warning("Please enter your Groq API Key in the sidebar.")
        else:
            with st.spinner("Saving campaign to database..."):
                payload = {
                    "name": campaign_name,
                    "prompt_template": prompt_template,
                    "recipients": st.session_state["recipient_data"],
                    "groq_api_key": groq_key
                }
                
                try:
                    response = requests.post(f"{BACKEND_URL}/api/campaign/start", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["campaign_id"] = data['id']
                        st.success(f"Success! Campaign '{data['name']}' created with ID: {data['id']}.")
                        st.info(f"{data['total_recipients']} recipient records have been saved to the database as 'Pending'.")
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend server.")

# Section 3: Review & Edit Drafts
if "campaign_id" in st.session_state:
    st.divider()
    st.header("Step 3: Review & Edit Drafts")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("Click refresh to fetch the latest AI-generated drafts from the database.")
    with col2:
        if st.button("Refresh Drafts"):
            # Trigger a rerun to fetch
            pass
            
    campaign_id = st.session_state["campaign_id"]
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaign/{campaign_id}/emails")
        if response.status_code == 200:
            emails = response.json()
            
            if not emails:
                st.info("No emails found yet. Ensure the Celery worker is running!")
            else:
                for idx, email in enumerate(emails):
                    # Use status for an indicator icon
                    if email["status"] == "sent":
                        icon = "Sent:"
                    elif email["status"] == "approved":
                        icon = "Approved:"
                    else:
                        icon = "Draft:"
                    
                    with st.expander(f"{icon} Email to: {email['recipient_name']} ({email['recipient_email']})"):
                        # We use session state to track edits per text area to avoid them overwriting on rerun
                        text_area_key = f"draft_{email['id']}"
                        
                        draft_content = email["generated_content"] if email["generated_content"] else "Waiting for AI..."
                        
                        # Fix for Streamlit caching: If the content updated in DB, force update session state
                        if text_area_key not in st.session_state or st.session_state.get(f"db_status_{email['id']}") != email["status"]:
                            st.session_state[text_area_key] = draft_content
                            st.session_state[f"db_status_{email['id']}"] = email["status"]
                            
                        edited_content = st.text_area(
                            "Edit Draft:", 
                            key=text_area_key,
                            height=200
                        )
                        
                        # Only show action buttons if the draft is actually generated
                        if email["status"] == "sent":
                            st.success("This email has been sent!")
                            
                        elif email["status"] == "approved":
                            st.info("Status: Approved — ready to send!")
                            col_a, col_b = st.columns([1, 1])
                            with col_a:
                                if st.button("Send Email Now", key=f"btn_send_{email['id']}", type="primary"):
                                    if not smtp_email or not smtp_password:
                                        st.error("Please enter your SMTP credentials in the sidebar.")
                                    else:
                                        with st.spinner("Sending..."):
                                            send_payload = {
                                                "smtp_email": smtp_email,
                                                "smtp_password": smtp_password
                                            }
                                            send_res = requests.post(f"{BACKEND_URL}/api/campaign/emails/{email['id']}/send", json=send_payload)
                                            if send_res.status_code == 200:
                                                st.balloons()
                                                st.success("Email sent successfully!")
                                                st.rerun()
                                            else:
                                                st.error(f"Failed to send: {send_res.text}")
                            with col_b:
                                if st.button("Edit & Re-save", key=f"btn_save_{email['id']}"):
                                    update_payload = {
                                        "generated_content": edited_content,
                                        "status": "approved"
                                    }
                                    res = requests.put(
                                        f"{BACKEND_URL}/api/campaign/emails/{email['id']}", 
                                        json=update_payload
                                    )
                                    if res.status_code == 200:
                                        st.success("Changes saved!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to save.")
                                        
                        elif email["status"] != "pending":
                            # Generated but not yet approved
                            st.warning("Draft generated — review and approve below.")
                            if st.button("Approve & Save", key=f"btn_save_{email['id']}", type="primary"):
                                update_payload = {
                                    "generated_content": edited_content,
                                    "status": "approved"
                                }
                                res = requests.put(
                                    f"{BACKEND_URL}/api/campaign/emails/{email['id']}", 
                                    json=update_payload
                                )
                                if res.status_code == 200:
                                    st.success("Approved!")
                                    st.rerun()
                                else:
                                    st.error("Failed to save.")
                                    
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to fetch emails.")
