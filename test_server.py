# server/test_server.py
import asyncio
from server.auth_utils import generate_token
from langchain_mcp_adapters.client import MultiServerMCPClient

TOKEN = generate_token("test-client")

async def test():
    config = {
        "local_server": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
            "headers": {
                "Authorization": f"Bearer {TOKEN}"
            }
        }
    }

    client = MultiServerMCPClient(config)
    tools = await client.get_tools()

    print("✅ Connected!")
    print(f"✅ Tools found: {[t.name for t in tools]}")

    

asyncio.run(test())