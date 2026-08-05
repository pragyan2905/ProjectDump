from typing import TypedDict
import os
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Clear out the broken shell variable so it doesn't override the .env file!
if "GROQ_API_KEY" in os.environ:
    del os.environ["GROQ_API_KEY"]

load_dotenv()

# 1. State Definition: The memory shared across all nodes for a single email generation
class EmailState(TypedDict):
    recipient_name: str
    recipient_email: str
    recipient_company: str
    recipient_role: str
    custom_prompt: str
    generated_draft: str
    quality_approved: bool

# Initialize Groq LLM (Ensure GROQ_API_KEY is set in your backend/.env)
# Using GPT-OSS 20B for high-quality text generation
llm = ChatGroq(
    temperature=0.7, 
    model_name="openai/gpt-oss-20b", 
    api_key=os.getenv("GROQ_API_KEY")
)

# 2. Node Functions
def draft_generator_node(state: EmailState):
    """Node: Generates the initial email draft based on recipient info and prompt."""
    
    prompt_template = PromptTemplate(
        input_variables=["name", "company", "role", "instructions"],
        template="""
        You are an expert sales/marketing AI. Write a personalized email.
        
        Recipient Details:
        Name: {name}
        Company: {company}
        Role: {role}
        
        Instructions/Purpose: 
        {instructions}
        
        Write only the email body and a 'Subject:' line. Be professional but friendly.
        """
    )
    
    chain = prompt_template | llm
    
    response = chain.invoke({
        "name": state.get("recipient_name", "Valued Contact"),
        "company": state.get("recipient_company", "your company"),
        "role": state.get("recipient_role", "your role"),
        "instructions": state["custom_prompt"]
    })
    
    return {"generated_draft": response.content}

def quality_inspector_node(state: EmailState):
    """Node: Verifies the draft isn't empty and contains a subject line."""
    draft = state.get("generated_draft", "")
    
    # In a production app, you might use another LLM call here to rate the email on a 1-10 scale.
    # We do a deterministic sanity check here for speed.
    if len(draft) > 50 and "subject:" in draft.lower():
        return {"quality_approved": True}
    return {"quality_approved": False}

# 3. Routing Logic
def route_approval(state: EmailState):
    if state["quality_approved"]:
        return "approved"
    return "rewrite"

# 4. Constructing the Graph
workflow = StateGraph(EmailState)

workflow.add_node("generator", draft_generator_node)
workflow.add_node("inspector", quality_inspector_node)

workflow.set_entry_point("generator")
workflow.add_edge("generator", "inspector")

# If approved, end. If rewrite, loop back to the generator.
workflow.add_conditional_edges(
    "inspector",
    route_approval,
    {
        "approved": END,
        "rewrite": "generator"
    }
)

# Compile into an executable agent
email_agent = workflow.compile()
