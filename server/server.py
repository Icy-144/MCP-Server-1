# server/server.py
import os
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers
from dotenv import load_dotenv
from auth_utils import verify_token

load_dotenv()

# Auth middleware using your HMAC verify_token from auth_utils.py
class HMACAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()

        auth_header = headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            raise ToolError("Unauthorized: Missing Bearer token")

        # Extract the raw token after "Bearer "
        token = auth_header[len("Bearer "):]

        # Use your HMAC verify_token from auth_utils.py
        client_id = verify_token(token)
        if not client_id:
            raise ToolError("Unauthorized: Invalid or expired token")

        # Token is valid — proceed
        return await call_next(context)


mcp = FastMCP("SecureServer", middleware=[HMACAuthMiddleware()])


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integer numbers together."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integer numbers together."""
    return a * b




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
    )