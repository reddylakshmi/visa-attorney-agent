import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import visa_agent
from langchain_core.messages import HumanMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    text: str

@app.post("/ask")
async def ask_legal_assistant(data: ChatInput):
    try:
        input_data = {"messages": [HumanMessage(content=data.text)]}
        result = await visa_agent.ainvoke(input_data)
        
        # 1. Grab the last message
        last_message = result["messages"][-1]
        raw_content = last_message.content

        # 2. THE CLEANER: Handle the [{'type': 'text', 'text': '...'}] format
        if isinstance(raw_content, list):
            # Extract 'text' from the first dictionary in the list
            clean_text = raw_content[0].get('text', str(raw_content))
        else:
            clean_text = str(raw_content)

        return {"reply": clean_text}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "I encountered an error processing that request."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)