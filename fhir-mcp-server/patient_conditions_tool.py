import json
import logging
from fhir_context import require_sharp_context

logger = logging.getLogger(__name__)

@require_sharp_context
async def get_patient_conditions(sharp_context=None):
    """
    Retrieves and parses active conditions/diagnoses from the FHIR server.
    Extracts only 'active' statuses and returns a clean list of condition displays.
    """
    logger.info(f"Querying conditions for patient: {sharp_context.patient_id}")
    
    # Mock Raw FHIR Bundle for robust parsing demonstration
    mock_fhir_bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Condition",
                    "clinicalStatus": {
                        "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
                    },
                    "code": {
                        "coding": [{"system": "http://snomed.info/sct", "code": "195967001", "display": "Asthma"}]
                    }
                }
            },
            {
                "resource": {
                    "resourceType": "Condition",
                    "clinicalStatus": {
                        "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "resolved"}]
                    },
                    "code": {
                        "coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Type 2 Diabetes"}]
                    }
                }
            },
            {
                "resource": {
                    "resourceType": "Condition",
                    "clinicalStatus": {
                        "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
                    },
                    "code": {
                        "coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}]
                    }
                }
            }
        ]
    }

    # 1. Parse FHIR Condition Bundle
    active_conditions = []
    for entry in mock_fhir_bundle.get("entry", []):
        resource = entry.get("resource", {})
        
        # Deep traversal of FHIR structure for clinicalStatus
        clinical_status_codings = resource.get("clinicalStatus", {}).get("coding", [])
        if not clinical_status_codings:
            continue
            
        status = clinical_status_codings[0].get("code")
        
        # Only extract if condition is 'active'
        if status == "active":
            code_codings = resource.get("code", {}).get("coding", [])
            if code_codings:
                display_name = code_codings[0].get("display")
                if display_name:
                    active_conditions.append(display_name)

    # Return clean list of active condition names
    return json.dumps({"conditions": active_conditions})
