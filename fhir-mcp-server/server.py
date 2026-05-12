import logging
import sys
import uvicorn

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from patient_vitals_tool import get_patient_vitals
from patient_conditions_tool import get_patient_conditions

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("fhir-mcp-server")

# --- FastMCP Server (Streamable HTTP) ---
mcp = FastMCP(
    "fhir-clinical-twin-mcp",
    host="0.0.0.0",
    port=8000,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    stateless_http=True,
)

@mcp.tool()
async def patient_vitals_tool() -> str:
    """Retrieve latest parsed patient vitals (HR, BP, O2). Requires SHARP context."""
    logger.info("Executing patient_vitals_tool")
    return await get_patient_vitals()

@mcp.tool()
async def patient_conditions_tool() -> str:
    """Retrieve active diagnoses filtered from Condition bundle. Requires SHARP context."""
    logger.info("Executing patient_conditions_tool")
    return await get_patient_conditions()

if __name__ == "__main__":
    logger.info("Starting FHIR MCP Server (Streamable HTTP) on port 8000...")
    mcp.run(transport="streamable-http")
