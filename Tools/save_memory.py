from langchain.tools import tool
from Schemas.memory_wrapper import memory_wrapper
from Memory.store import store
import Utils.status_manager as status_manager
import time

@tool("save_memory", description="Save important information", args_schema=memory_wrapper)
def save_memory(memory: memory_wrapper):
    status_manager.add_status("saving memory for future calls...")
    time.sleep(1)
    
    saved_memory = []
    for item in memory:
        memory_data = f"{item.key} : {item.value}"
        saved_memory.append(memory_data)
        
    readable_memory = ', '.join(saved_memory)
    print('[Readable Memory] : ', readable_memory)
    
    existing_memory = store.get(("user_123", "memories"), "123")
    
    if existing_memory and readable_memory:
        combined_text = readable_memory + " | " + existing_memory.value['text']
    else:
        combined_text = readable_memory + existing_memory.value['text']

    store.put(("user_123", "memories"), "123", {'text': combined_text})
    
    print("memory saved: ", ", ".join(saved_memory))
    
    status_manager.add_status("Memory Saved")
    time.sleep(1)
    
    return ", ".join(saved_memory) 