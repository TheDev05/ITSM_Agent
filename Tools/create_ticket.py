from langchain.tools import tool
import Utils.status_manager as status_manager
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import time
from Memory.store import store

@tool("create_servicenow_ticket", return_direct = False)
def create_ticket(short_description: str, description: str):
    """
    Creates a ServiceNow incident ticket.
    Returns the ticket number.
    """
    
    sys_id = ""
    
    status_manager.add_status("creating servicenow ticket for user issue...")
    time.sleep(2)
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/incident"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    user_data = store.get(("user_123", 'credentials'), "123")

    if user_data:
        print("User exists", user_data.value['sys_id'])
        sys_id = user_data.value['sys_id'] 
    else:
        print('User doesnot exist')

    payload = {
        "short_description": short_description, 
        "description": description,
        "caller_id": sys_id
    }

    response = requests.post(url, auth=(os.getenv('SERVICENOW_USER'), os.getenv('SERVICENOW_PASS')), headers=headers, json=payload)

    if response.status_code == 201:
        ticket_number = response.json()["result"]["number"]  
        
        status_manager.add_status("ticket generated succesfully")
        time.sleep(2)
        
        return f"Ticket created with Ticket Number {ticket_number}. Anything else I can help you?"
    else:
        print(f"ServiceNow API error {response.status_code}")
        return f"There is some issue with connection now, Try after some time"