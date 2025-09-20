from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState
from Models.model import model
from dotenv import load_dotenv

from Prompts.SYSTEM_PROMPT import SYSTEM_PROMPT
from Tools.add_integers import add_integers
from Tools.save_memory import save_memory
from Tools.get_memory import get_memory
from Tools.create_ticket import create_ticket
from Tools.fetch_all_tickets import fetch_all_tickets
from Tools.get_internal_informations import get_internal_information
from Utils.load_mcp_tools import load_mcp_tools
from Memory.store import store
from State.agentState import agentState

load_dotenv() 

tools = [get_memory, save_memory, add_integers, get_internal_information]

async def get_agent(state: agentState):
    
    mcp_tools = await load_mcp_tools()
    all_tools = tools + mcp_tools
    # print("tools: ", all_tools)
    
    agent = create_react_agent(tools = all_tools, model = model, prompt = SYSTEM_PROMPT)
    
    filtered = [m for m in state["messages"] if m.type in ["system", "human", "ai"]]
    response = await agent.ainvoke({"messages": filtered})
    
    return {'messages': [response["messages"][-1]]}