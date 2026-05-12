import json
import logging
try:
    from google_adk.agent import Agent
    from google_adk.orchestration import A2AOrchestrator
    from google_adk.llm import LLMConfig
except ImportError:
    # Provide dummy classes if not installed to prevent script crashing locally
    class Agent:
        def __init__(self, **kwargs): pass
    class A2AOrchestrator:
        def __init__(self, **kwargs): pass
    class LLMConfig:
        def __init__(self, **kwargs): pass

import websockets
import random
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fhir-a2a-agent")

class ClinicalTwinAgent(Agent):
    """
    The 'Superhero' Agent (Layer B) that connects the frontend to the MCP tools.
    """
    def __init__(self):
        super().__init__(
            name="ClinicalTwinOrchestrator",
            description="Processes requests from the frontend UI and triggers MCP tools to fetch raw FHIR data.",
            llm_config=LLMConfig(model="gemini-2.5-flash")
        )
        
    async def process_frontend_request(self, request_payload: dict) -> dict:
        """
        Listens for requests from the frontend UI, delegates to the MCP server,
        and formats the resulting data for the 3D representation.
        """
        logger.info("Received request from React UI")
        
        # 1. Trigger the MCP tools (Layer A) via A2A Orchestrator
        # Note: In the Prompt Opinion platform, the SHARP context is automatically 
        # propagated when we call out to the MCP server tool from here.
        
        logger.info("Calling patient_vitals_tool via MCP...")
        # Mocking parsed response returned from rewritten MCP Server
        vitals_data = {
            "heart_rate": {"value": 82, "unit": "beats/min"},
            "bp_systolic": {"value": 120, "unit": "mmHg"},
            "bp_diastolic": {"value": 80, "unit": "mmHg"},
            "spo2": {"value": 98, "unit": "%"}
        }
        
        logger.info("Calling patient_conditions_tool via MCP...")
        # Clean list of strings from updated Condition tool
        conditions_data = {
            "conditions": ["Asthma", "Hypertension"]
        }
        
        # 2. Generate the consolidation structure exactly how Frontend prefers it
        active_conditions = conditions_data["conditions"]
        highlighted_meshes = self._map_conditions_to_meshes(active_conditions)
        
        formatted_ui_state = {
            "vitals": {
                "heartRate": f"{vitals_data['heart_rate']['value']}",
                "bloodPressure": f"{vitals_data['bp_systolic']['value']}/{vitals_data['bp_diastolic']['value']}",
                "spo2": f"{vitals_data['spo2']['value']}",
            },
            "conditions": active_conditions,
            "highlighted_meshes": highlighted_meshes
        }
        
        logger.info(f"Consolidated payload generated. Highlighted systems: {highlighted_meshes}")
        return formatted_ui_state
        
    def _map_conditions_to_meshes(self, conditions: list) -> list:
        """
        Maps validated condition display names to human-readable model target keys.
        """
        mapping = []
        for condition in conditions:
            normalized = condition.lower()
            if "asthma" in normalized or "copd" in normalized:
                mapping.append("Lungs")
            elif "hypertension" in normalized or "heart" in normalized:
                mapping.append("Heart")
        return mapping

async def broadcast_handler(websocket):
    """Handle websocket streaming loop for the clinical state."""
    logger.info(f"UI Client connected: {websocket.remote_address}")
    agent = ClinicalTwinAgent()
    
    try:
        while True:
            # Simulate slight vital fluctuation
            hr_val = 82 + random.randint(-2, 5)
            bp_sys = 120 + random.randint(-5, 10)
            
            # Explicitly get standard formatted state
            # In full stack this would trigger actual tool calls
            state = await agent.process_frontend_request({"action": "stream_state"})
            
            # Inject variation so viewer sees real time flux
            state["vitals"]["heartRate"] = str(hr_val)
            state["vitals"]["bloodPressure"] = f"{bp_sys}/80"
            
            await websocket.send(json.dumps(state))
            await asyncio.sleep(1.5)
    except websockets.ConnectionClosed:
        logger.info("UI Client disconnected")

async def main():
    logger.info("Initializing Mock Orchestrator for WebSocket streaming on ws://localhost:8765")
    async with websockets.serve(broadcast_handler, "localhost", 8765):
        await asyncio.Future() # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down server.")
