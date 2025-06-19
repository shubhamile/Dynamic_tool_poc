import os
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_swarm
from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.langchain import CallbackHandler
from langgraph.types import interrupt
from pydantic import BaseModel
from dto import Community, Home
import generate_basetool
from tools.generate_filters import retrieve_details_from_mongodb

os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-fc1f05d4-b8da-40a3-9c00-9d44431c03c0" 
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-152c9bcb-d334-4525-9567-945c7fe809e7" 
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

langfuse_handler = CallbackHandler()

#Generate Community filter tools
# class CommunityModel(BaseModel):
#     filters:Community
    
class CommunityFilter(BaseModel):
    mongo_details:Community

community_tool = generate_basetool.create_tool(func=retrieve_details_from_mongodb, args_schema=CommunityFilter, name="community_filter_tool", description="Capture all the community filters.",  return_format="content_and_artifact")

#Generate home filter tools
class HomeModel(BaseModel):
    mongo_details:Home
home_tool = generate_basetool.create_tool(func=retrieve_details_from_mongodb, args_schema=HomeModel, name="home_filter_tool", description="Capture all the home filters.",  return_format="content_and_artifact")


os.environ["GOOGLE_API_KEY"] = "AIzaSyC4caXCogyYT2FQ00NLLx5ttd0n8hnq-fQ"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

property_agent = create_react_agent(
    model=llm,
    tools=[community_tool, home_tool],
    name="property_info_agent",
    prompt=(
        "You are a property data agent. Your role is to manage and process structured property data including "
        "purchase types, prices, rental details, features, amenities, and community information.\n\n"
        "Respond briefly and politely if the user greets you (e.g., 'hi', 'hello', 'good morning'), and do not call any tool.\n\n"
        "Use the correct tool:\n"
        "- Use **Extract_Community_info** for community-related data queries (e.g., locations, communities, societies).\n"
        "- Use **Extract_home_info** for individual home/property-related details (e.g., bedrooms, rent, sale).\n"
    )
)

checkpoint = InMemorySaver()
supervisor = create_swarm(
    agents=[property_agent],
    default_active_agent="property_info_agent",
)

# supervisor = create_supervisor(
#     [property_agent],
#     model=llm,
#     prompt=(
#         "You are a smart team supervisor managing an expert agent named 'property_info_agent'. "
#         "This agent is responsible for handling all property-related queries.\n\n"
        
#         "If the user greets (e.g., says 'hi', 'hello', etc.), respond briefly and politely without calling any agent.\n"
        
#         "For any message related to properties, homes, rentals, or communities, route the query to 'property_info_agent'.\n\n"
        
#         "Do not attempt to answer property-specific queries yourself. Always delegate them to the agent."
#     )
# )


graph = supervisor.compile(checkpointer=checkpoint)

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}, "checkpoint_ns": thread_id, "callbacks": [langfuse_handler]}

print("==========================", graph.get_state(config), "=========================")