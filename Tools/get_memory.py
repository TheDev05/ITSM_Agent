from langchain.tools import tool
import Utils.status_manager as status_manager
from Memory.store import store
import time

@tool("get_memory", description="Fetch relevant memory")
def get_memory(query: str):
    status_manager.add_status("looking for relevant memory...")
    time.sleep(1)
    
    memory = []
    items = store.search(("user_123", "memories"), query=query, limit=3)
    
    if not items:
        status_manager.add_status("memory not found, generating response")
        time.sleep(1)
        
        return "No Memories Found"
    
    print('[Memory] : ', items)
    for item in items:
        memory.append(item.value['text'])
    
    result = "\n".join(memory)
    print("memory called: ", result)
    
    status_manager.add_status("memory found, generating response")
    time.sleep(1)
    
    return result