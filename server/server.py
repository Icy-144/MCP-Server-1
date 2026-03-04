# server/server.py
import os
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_request
from dotenv import load_dotenv
from auth_utils import verify_token

load_dotenv()


class HMACAuthMiddleware(Middleware):

    async def on_request(self, context: MiddlewareContext, call_next):
        try:
            # Use get_http_request() instead of get_http_headers()
            request = get_http_request()
            auth_header = request.headers.get("authorization", "")
        except Exception:
            # No HTTP request context (e.g. during initialization) — let it through
            return await call_next(context)

        # Only check requests that carry an Authorization header check
        if not auth_header:
            return await call_next(context)

        if not auth_header.startswith("Bearer "):
            raise ToolError("Unauthorized: Missing Bearer token")

        token = auth_header[len("Bearer "):]
        client_id = verify_token(token)

        if not client_id:
            raise ToolError("Unauthorized: Invalid or expired token")

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