from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langgraph.checkpoint.memory import MemorySaver
import json
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


memory = MemorySaver()

agent_app = FastAPI()

load_dotenv()
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION_ENV")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT_ENV")
AZURE_API_KEY = os.getenv("AZURE_API_KEY_ENV")

def llm():
    model = AzureChatOpenAI(
        api_version= AZURE_API_VERSION,
        azure_endpoint= AZURE_ENDPOINT,
        api_key= AZURE_API_KEY,
        azure_deployment="gpt-4o",
        verbose=True
    )
    return model

azure_api_client = llm()



@agent_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint"""
    await websocket.accept()
    print("client Connected")
    try:
        while True:
            payload = await websocket.receive_text()
            data = json.loads(payload)
            user_query = data.get('query')
            session_id = data.get('id')
            
            # Connect to MCP server and get tools
            async with MultiServerMCPClient(
                {
                    "os_tool_server": {
                        "url": "http://localhost:8003/sse",
                        "transport": "sse",
                    }
                }
            ) as client:
                tools = client.get_tools()
                
                # Create agent with tools
                agent = create_react_agent(
                    azure_api_client, 
                    tools, 
                    checkpointer=memory
                )
                
                # Process the query
                config = {"configurable": {"thread_id": session_id}}
                response = await agent.ainvoke(
                    {"messages": [{"role": "user", "content": user_query}]},
                    config=config
                )
                
                # Extract the final response
                final_response = ""
                for msg in response['messages']:
                    if hasattr(msg, 'content') and msg.content:
                        final_response = msg.content
                
                # Send response back to client
                await websocket.send_text(json.dumps({
                    "response": final_response,
                    "session_id": session_id
                }))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(json.dumps({
            "error": str(e),
            "session_id": session_id if 'session_id' in locals() else None
        }))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(agent_app, host="0.0.0.0", port=8004)
