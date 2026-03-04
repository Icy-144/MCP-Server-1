# server/test_server.py
import asyncio
import os
from server.auth_utils import generate_token
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

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

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.environ["GROQ_API_KEY"],
    )

    agent = create_agent(model=model, tools=tools)

    print("\n--- Test: add ---")
    result = await agent.ainvoke({"messages": "What is 5 plus 3? Use the add tool."})
    print(f"✅ Result: {result['messages'][-1].content}")

    print("\n--- Test: multiply ---")
    result = await agent.ainvoke({"messages": "What is 4 multiplied by 6? Use the multiply tool."})
    print(f"✅ Result: {result['messages'][-1].content}")


asyncio.run(test())