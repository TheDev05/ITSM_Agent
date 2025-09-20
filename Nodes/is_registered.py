from langgraph.graph import MessagesState
from dotenv import load_dotenv
import requests
import os

from Memory.store import store
import Utils.status_manager as status_manager
from Utils.redis import redis_client
from State.agentState import agentState

load_dotenv() 

def is_registered(state: agentState):
    user_data = store.get(("user_123", 'credentials'), "123") 
    print("[TRACK user_data] : ", user_data)
    
    human_decision = state.get("human_decision", None)
    if user_data.value.get("sys_id") or human_decision is False:
        print('[TRACK] : user found going to agent_node')
        return 'get_agent'

    print('[TRACK] : sys_id doesnot found in memory')
    
    email = user_data.value['email']
    status_manager.add_status("validating user...")
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/sys_user"
    headers = {"Accept": "application/json", "Content-Type": "application/json"} 
        
    params = {
        "sysparm_query": f"email={email}", 
        "sysparm_fields": "sys_id,email,name" 
    }

    response = requests.get(url, auth=(os.getenv('SERVICENOW_USER'), os.getenv('SERVICENOW_PASS')), params=params) 
    data = response.json()

    if data.get("result"):
        print("[TRACK] : User exists at servicenow, sys_id stored locally")
        status_manager.add_status("user exists at servicenow")
        
        sys_id = data["result"][0]['sys_id']
        
        user_data = store.get(("user_123", 'credentials'), "123") 
        print("[TRACK BEFORE user_data] : ", user_data)
        
        store.put(("user_123", 'credentials'), "123", {
            "sys_id": sys_id,
            **user_data.value,
            }) 
        
        print("[TRACK sys_id] : ", sys_id)
        
        user_data = store.get(("user_123", 'credentials'), "123") 
        print("[TRACK user_data] : ", user_data)
        
        redis_client.set(f"user:{email}", sys_id)
        print(f'[REDIS] : user sys_id saved in redis for user {email}')

        return 'get_agent'
    else:
        print("[TRACK] : User doesnot exists at servicenow, return register_user")
        status_manager.add_status("user doesnot exists at servicenow")
        
        return 'get_hitl_response'