import logging
import sys
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import Tool

from patient_vitals_tool import get_patient_vitals
from patient_conditions_tool import get_patient_conditions

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("fhir-mcp-server")

# --- MCP Server Definition ---
app = Server("fhir-clinical-twin-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return tool definitions for the MCP client."""
    return [
        Tool(
            name="patient_vitals_tool",
            description="Retrieve latest parsed patient vitals (HR, BP, O2). Requires SHARP context.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="patient_conditions_tool",
            description="Retrieve active diagnoses filtered from Condition bundle. Requires SHARP context.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    logger.info(f"Executing tool: {name}")
    try:
        if name == "patient_vitals_tool":
            result = await get_patient_vitals()
            return [{"type": "text", "text": result}]
        elif name == "patient_conditions_tool":
            result = await get_patient_conditions()
            return [{"type": "text", "text": result}]
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Tool error: {e}")
        return [{"type": "text", "text": f"Error: {e}"}]


# --- SSE Transport Setup ---
# IMPORTANT: Use trailing slash "/messages/" so that:
#   1) SseServerTransport tells the client to POST to "/messages/?session_id=..."
#   2) Mount("/messages/") matches that path directly — NO 307 redirect
transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
sse = SseServerTransport("/messages/", security_settings=transport_security)


async def handle_sse(request):
    """SSE endpoint — client connects here to receive the event stream."""
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send
    ) as streams:
        logger.info("SSE client connected.")
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )
    return Response()


async def handle_health(request):
    """Health check endpoint — PromptOpinion probes '/' before connecting to /sse."""
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "ok", "server": "fhir-clinical-twin-mcp", "transport": "sse"})


# --- Starlette App ---
starlette_app = Starlette(
    debug=False,
    routes=[
        Route("/", endpoint=handle_health, methods=["GET"]),
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    logger.info("Starting FHIR MCP Server (SSE) on port 8000...")
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)
