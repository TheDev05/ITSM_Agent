from langgraph.types import Command, interrupt
from State.agentState import agentState

def get_hitl_response(state: agentState):
    print('[TRACK] : HITL Node Invoked')
    
    human_decision = interrupt({
        "prompt": "Hi, It seems you are not registered to us, Allow me to create your account!", 
        "text": "You are not registred to us."
    })
    
    print(f"[DEBUG] : Received human decision: {human_decision}")
    return {"human_decision": human_decision}