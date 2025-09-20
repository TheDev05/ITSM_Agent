from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from dotenv import load_dotenv

import os

from RAG.embedding import persist_documents
from Memory.store import store
from Nodes.Human_In_The_Loop import get_hitl_response
from Nodes.register_user import register_user
from Nodes.is_registered import is_registered
from Nodes.get_agent import get_agent
from State.agentState import agentState
from Nodes.is_human_decided import is_human_decided
from State.agentState import agentState

load_dotenv() 

graph = StateGraph(agentState)

graph.add_node("get_agent", get_agent)
graph.add_node('register_user', register_user) 
graph.add_node('get_hitl_response', get_hitl_response)

graph.add_conditional_edges(START, is_registered)
graph.add_conditional_edges('get_hitl_response', is_human_decided)
graph.add_edge('register_user', 'get_agent')
graph.add_edge("get_agent", END)

checkpointer = InMemorySaver()
config = {'configurable': {'thread_id': '1'}}
workflow = graph.compile(checkpointer = checkpointer, store = store)

async def run_workflow(query: str):
    response = await workflow.ainvoke({'messages': [HumanMessage(content = query)]}, config = config)        
    # print('response 1: ', response)
    if "__interrupt__" in response:
        print('[TRACK] : Interrupt generated, Workflow Paused')
        return response
    else:
        print('[TRACK] : HITL trigerred already, No Interruption this Time')
        return response['messages'][-1].content

async def resume_workflow(query: str, human_input):
    response = await workflow.ainvoke(Command(resume = human_input), config = config)
    # print('response 2: ', response)
    print('[TRACK] : used HITL response - Approved, Resumed workflow')
    return response['messages'][-1].content

if __name__ == "__main__":
    if not os.path.exists('./persit'):
        print("[TRACK] : Document Embedding Generated")
        persist_documents()
