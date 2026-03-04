# client/client.py
import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient


load_dotenv()

MCP_SERVER_URL = os.environ["MCP_SERVER_URL"]
MCP_TOKEN      = os.environ["MCP_TOKEN"]


async def run_agent():

    # Server configuration dictionary
    # Each key is a name you give to identify the server connection
    # You can add as many servers as needed under different keys
    config = {
        "secure_mcp_server": {
            "url": MCP_SERVER_URL,       # must end in /sse
            "transport": "streamable_http",
            "headers": {
                "Authorization": f"Bearer {MCP_TOKEN}"
            },
        },

        # Add more servers here if needed:
        # "another_server": {
        #     "url": "https://other-server.onrender.com/sse",
        #     "transport": "sse",
        #     "headers": {"Authorization": "Bearer <other_token>"},
        # },
    }


    # Create the client and fetch tools
    client = MultiServerMCPClient(config)
    tools  = await client.get_tools()

    print(f"\n✅ Connected to MCP Server!")
    print(f"📦 Available tools ({len(tools)} total):")
    for tool in tools:
        print(f"   • {tool.name}: {tool.description}")



if __name__ == "__main__":
    asyncio.run(run_agent())