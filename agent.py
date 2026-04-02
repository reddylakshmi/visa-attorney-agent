import os
import operator
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

# 1. Load environment variables from .env
load_dotenv()

# 2. Define the Agent's state (memory)
class AgentState(TypedDict):
    # Annotated with operator.add tells LangGraph to append new messages to history
    messages: Annotated[List[BaseMessage], operator.add]

# 3. Initialize the Google Gemini Model
# We use 'gemini-3.1-flash-lite-preview' which is the current 2026 free-tier workhorse
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2, # Lower temperature for more factual legal responses
)

# 4. Define the Attorney Node (The Brain)
def attorney_node(state: AgentState):
    """
    Processes the conversation and generates a professional legal response.
    """
    system_prompt = SystemMessage(content=(
        "You are a professional US Immigration Attorney Assistant. "
        "Provide clear, accurate information regarding H1B, B1/B2, F1, J1, and L1 visas. "
        "\n\nRULES:\n"
        "1. Always include a legal disclaimer: 'I am an AI assistant, not an attorney. "
        "This information is for educational purposes and does not constitute legal advice.'\n"
        "2. Cite official USCIS or Department of State terminology.\n"
        "3. If a question is outside US Immigration, politely decline to answer."
    ))
    
    # Combine system prompt with the message history
    all_messages = [system_prompt] + state["messages"]
    
    # Call Gemini
    response = llm.invoke(all_messages)
    
    # Return the new message to be added to the state
    return {"messages": [response]}

# 5. Build the LangGraph Workflow
workflow = StateGraph(AgentState)

# Add our node to the graph
workflow.add_node("attorney_assistant", attorney_node)

# Define the flow: Start -> Attorney -> End
workflow.add_edge(START, "attorney_assistant")
workflow.add_edge("attorney_assistant", END)

# 6. Compile the graph into an executable agent
visa_agent = workflow.compile()