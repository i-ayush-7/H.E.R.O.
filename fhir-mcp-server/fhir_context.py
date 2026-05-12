import json
import os
import functools

class SHARPContext:
    """
    Implements the SHARP (Secure Healthcare Agent Request Protocol) Extension Specs.
    Extracts secure healthcare context (Patient IDs and FHIR tokens) propagated 
    through multi-agent call chains by the Prompt Opinion platform.
    """
    def __init__(self, patient_id=None, fhir_token=None):
        self.patient_id = patient_id
        self.fhir_token = fhir_token

    @classmethod
    def from_env(cls):
        """
        In the Prompt Opinion platform, when 'Requires Patient Data Access' is toggled ON,
        the platform injects SHARP context securely into the execution environment or via MCP metadata.
        For local testing, we can simulate this with environment variables.
        """
        patient_id = os.environ.get("SHARP_PATIENT_ID")
        fhir_token = os.environ.get("SHARP_FHIR_TOKEN")
        return cls(patient_id=patient_id, fhir_token=fhir_token)

    @classmethod
    def from_mcp_request(cls, request_meta):
        """
        Extracts SHARP context directly from the MCP request metadata.
        This handles the token propagation without bespoke token vaults.
        """
        if not request_meta or "sharp_context" not in request_meta:
            # Fallback to env for local dev
            return cls.from_env()
            
        sharp_data = request_meta.get("sharp_context", {})
        return cls(
            patient_id=sharp_data.get("patient_id"),
            fhir_token=sharp_data.get("fhir_token")
        )

def require_sharp_context(func):
    """
    Decorator to ensure the SHARP context is available before executing a tool.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # In a real MCP handler, context might be passed in kwargs or accessible via a request object
        # Here we mock extraction for the tool signatures
        context = SHARPContext.from_env()
        if not context.fhir_token or not context.patient_id:
            raise ValueError("Unauthorized: Missing SHARP context (FHIR token or Patient ID). Ensure 'Requires Patient Data Access' is toggled ON.")
        
        # Inject context into kwargs
        kwargs['sharp_context'] = context
        return await func(*args, **kwargs)
    return wrapper
