from State.agentState import agentState

def is_human_decided(state: agentState):
    if state['human_decision']:
        return 'register_user'
    else:
        return 'get_agent'