from langchain.tools import tool
from Schemas.add_integers import addition_schema
import Utils.status_manager as status_manager

@tool("addition", description = "add two integers", args_schema = addition_schema)
def add_integers(a: int, b: int):
    status_manager.add_status("add_integers called")
    status_manager.add_status("Sum Returned")
    return a + b
