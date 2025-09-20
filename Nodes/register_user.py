from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState
import requests
import os

from Memory.store import store
import Utils.status_manager as status_manager
from Utils.redis import redis_client
from State.agentState import agentState

def register_user(state: agentState):
    user_data = store.get(("user_123", 'credentials'), "123")
    email = user_data.value['email']
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/sys_user"
    headers = {"Accept": "application/json", "Content-Type": "application/json"} 
    
    payload = {
            "name": user_data.value['name'],
            "email": user_data.value['email'],
        }

    response = requests.post(url, auth=(os.getenv('SERVICENOW_USER'), os.getenv('SERVICENOW_PASS')), headers=headers, json=payload)

    print(response.json())
    if response.status_code == 201:
        sys_id = response.json()["result"]["sys_id"]
        store.put(("user_123", 'credentials'), "123", {
        "sys_id": sys_id,
        **user_data.value,  
        })
        
        redis_client.set(f"user:{email}", sys_id)
        print(f'[REDIS] : user sys_id saved in redis for user {email}')
        
        
        print('[TRACK] : user created in servicenow, sys_id stored locally')
        status_manager.add_status("user profile created at servicenow")
    else:
        print(f"Some Error occurs during user's registration {response.status_code}")
    
    return {'messages' : [AIMessage(content = 'user registred')]}