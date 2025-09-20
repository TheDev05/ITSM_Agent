from langchain.tools import tool
import Utils.status_manager as status_manager
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import time
from Memory.store import store

@tool("fetch_all_tickets", return_direct=False)
def fetch_all_tickets(short_description: str, description: str):
    """
    Fetch all ServiceNow incident tickets for the user.
    Returns all the ticket number with short details.
    """
    
    user_data = store.get(("user_123", 'credentials'), "123")
    sys_id = user_data.value['sys_id']
    
    status_manager.add_status("fetching servicenow tickets for the user...")
    time.sleep(2)
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/incident"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    user_data = store.get(("user_123", 'credentials'), "123")

    if user_data:
        print("User exists", user_data.value['sys_id'])
        sys_id = user_data.value['sys_id']
    else:
        print('User doesnot exist')

    params = {
        "sysparm_query": f"caller_id={sys_id}",
        "sysparm_fields": "number, short_description, state",
        "sysparm_limit": 100
    }

    response = requests.get(url, auth=(os.getenv('SERVICENOW_USER'), os.getenv('SERVICENOW_PASS')), headers=headers, params=params)

    if response.status_code == 200:
        tickets = response.json()["result"] 
        result = []
        for t in tickets:
            result.append(f"{t['number']} | {t['short_description']} | State: {t['state']}")
        return result
    else:
        print(f"Error fetching tickets: {response.status_code} - {response.text}")