from langchain_mcp_adapters.client import MultiServerMCPClient

async def load_mcp_tools(): 
    client = MultiServerMCPClient(
        {
            "servicenow" : {
                "url" : "http://127.0.0.1:8000/mcp",
                "transport" : "streamable_http"
            }
        }
    )
    
    mcp_tools = await client.get_tools()
    return mcp_tools