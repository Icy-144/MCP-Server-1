# server/test_server.py
import asyncio
import os
from server.auth_utils import generate_token
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

VALID_TOKEN   = generate_token("test-client")
INVALID_TOKEN = "fake-token-123"


async def test_valid():
    print("\n--- Test 1: Valid Token ---")
    config = {
        "local_server": {
            "url": "https://mcp-server-1-fi5a.onrender.com/mcp",
            "transport": "http",
            "headers": {
                "Authorization": f"Bearer {VALID_TOKEN}"
            }
        }
    }

    client = MultiServerMCPClient(config)
    tools  = await client.get_tools()

    print(f"✅ Connected! Tools: {[t.name for t in tools]}")

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.environ["GROQ_API_KEY"],
    )

    agent = create_agent(model=model, tools=tools)

    result = await agent.ainvoke({"messages": "What is 5 plus 3? Use the add tool."})
    print(f"✅ add result: {result['messages'][-1].content}")

    result = await agent.ainvoke({"messages": "What is 4 multiplied by 6? Use the multiply tool."})
    print(f"✅ multiply result: {result['messages'][-1].content}")


async def test_invalid():
    print("\n--- Test 2: Invalid Token (should be blocked) ---")
    config = {
        "local_server": {
            "url": "https://mcp-server-1-fi5a.onrender.com/mcp",
            "transport": "http",
            "headers": {
                "Authorization": f"Bearer {INVALID_TOKEN}"
            }
        }
    }
    try:
        client = MultiServerMCPClient(config)
        await client.get_tools()
        print("❌ ERROR: Should have been blocked")
    except Exception as e:
        print(f"✅ Correctly blocked: {e}")


async def main():
    await test_valid()
    await test_invalid()


asyncio.run(main())