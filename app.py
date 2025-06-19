import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent_core import config, graph
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import StateSnapshot, Command

app = FastAPI()
# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class MessageInput(BaseModel):
    message: str
    
def has_interrupt(snapshot: StateSnapshot) -> bool:
    return any(task.interrupts for task in snapshot.tasks or [])


@app.post("/ask")
async def ask_property_agent(payload: MessageInput):
    start_time = time.perf_counter()

    print("==========================", graph.get_state(config), "=========================")
    
    # Get current state of the graph
    state = graph.get_state(config=config)

    # If interrupted last time, resume
    if has_interrupt(snapshot=state):
        result = graph.invoke(
            Command(resume={"data": payload.message}),
            config=config
        )
    else:
        inputs = {"messages": [("user", payload.message)]}
        result = graph.invoke(inputs, config=config)

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.4f} seconds")

    final_response = ""
    print(f"################## {result} ###############")
    # Filter AI messages only
    if '__interrupt__' in result and result['__interrupt__']:
        interrupts = result.get("__interrupt__", [])
        if interrupts:
            final_response = interrupts[0].value
    else:
        final_response = next(
            (m.content for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
            "Sorry, I couldn't find a valid response."
        )

    return {"response": final_response}