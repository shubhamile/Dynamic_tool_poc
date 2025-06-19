# Dynamic_tool_poc

🧠 AI Agent API (FastAPI + LangGraph)
=====================================

A simple FastAPI server that wraps a LangGraph-based AI agent to handle user queries with stateful conversation and interrupt handling.

🚀 Setup
--------
pip install fastapi uvicorn pydantic langgraph langchain
uvicorn main:app --reload

📬 Endpoint
-----------
POST /ask

Request:
{
  "message": "I need a house in Miami"
}

Response:
{
  "response": "Sure! What's your budget or preferred area?"
}

🧪 Test with Curl
-----------------
curl -X POST http://localhost:8000/ask \\
  -H "Content-Type: application/json" \\
  -d '{"message": "I need a house in Miami"}'
