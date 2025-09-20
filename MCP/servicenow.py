from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

import os
import requests
import redis

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True,
    username=os.getenv('REDIS_USER'),
    password=os.getenv('REDIS_PASS'),
)

mcp = FastMCP('servicenow tools')

@mcp.tool("create_servicenow_ticket")
def create_ticket(short_description: str, description: str, email: str):
    """
    Creates a ServiceNow incident ticket.
    Returns the ticket number.
    
    Args:
        email: The user's email
    """
    
    print('[TRACK] : fetch all tickets called')
    
    sys_id = redis_client.get(f"user:{email}")
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/incident"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "short_description": short_description, 
        "description": description,
        "caller_id": sys_id
    }

    response = requests.post(url, auth=(os.getenv('SERVICENOW_USER'), os.getenv('SERVICENOW_PASS')), headers=headers, json=payload)

    if response.status_code == 201:
        ticket_number = response.json()["result"]["number"]  
        
        return f"Ticket created with Ticket Number {ticket_number}. Anything else I can help you?"
    else:
        print(f"ServiceNow API error {response.status_code}")
        return f"There is some issue with connection now, Try after some time"
    

@mcp.tool("fetch_all_tickets", description="Fetch all ServiceNow incident tickets for the user")
def fetch_all_tickets(email: str):
    """
    Fetch all ServiceNow incident tickets for the user.
    Returns all the ticket number with short details.
    
    Args:
        email: The user's email
    """

    print('[TRACK] : fetch all tickets called')

    sys_id = redis_client.get(f"user:{email}")
    
    url = f"{os.getenv('SERVICENOW_URL')}/api/now/table/incident"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

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
        
if __name__ == "__main__":
    mcp.run(transport = "streamable-http")
    