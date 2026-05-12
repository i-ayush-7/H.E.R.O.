import json
import logging
from fhir_context import require_sharp_context

logger = logging.getLogger(__name__)

@require_sharp_context
async def get_patient_vitals(sharp_context=None):
    """
    Retrieves and parses latest vitals from a FHIR Observation bundle.
    Extracts values and units for Heart Rate, Blood Pressure, and SpO2 by LOINC codes.
    """
    logger.info(f"Querying vitals for patient: {sharp_context.patient_id}")
    
    # Mock Raw FHIR Observation Bundle (Standard LOINC codes)
    mock_fhir_bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
                    "valueQuantity": {"value": 82, "unit": "beats/min"}
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "code": {"coding": [{"system": "http://loinc.org", "code": "2708-6", "display": "Oxygen saturation in Arterial blood"}]},
                    "valueQuantity": {"value": 98, "unit": "%"}
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "code": {"coding": [{"system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel with all children optional"}]},
                    "component": [
                        {
                            "code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]},
                            "valueQuantity": {"value": 120, "unit": "mmHg"}
                        },
                        {
                            "code": {"coding": [{"system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure"}]},
                            "valueQuantity": {"value": 80, "unit": "mmHg"}
                        }
                    ]
                }
            }
        ]
    }

    parsed_vitals = {}
    
    # 1. Iterate and parse Observations based on common LOINC mappings
    for entry in mock_fhir_bundle.get("entry", []):
        obs = entry.get("resource", {})
        codings = obs.get("code", {}).get("coding", [])
        if not codings:
            continue
            
        loinc_code = codings[0].get("code")
        
        # Single Value Observations
        if "valueQuantity" in obs:
            val = obs["valueQuantity"].get("value")
            unit = obs["valueQuantity"].get("unit")
            
            if loinc_code == "8867-4": # Heart Rate
                parsed_vitals["heart_rate"] = {"value": val, "unit": unit}
            elif loinc_code == "2708-6": # SpO2
                parsed_vitals["spo2"] = {"value": val, "unit": unit}
                
        # Panel/Compound Observations (like Blood Pressure)
        elif "component" in obs:
            for comp in obs.get("component", []):
                comp_codings = comp.get("code", {}).get("coding", [])
                if not comp_codings: continue
                
                comp_loinc = comp_codings[0].get("code")
                comp_val = comp.get("valueQuantity", {}).get("value")
                comp_unit = comp.get("valueQuantity", {}).get("unit")
                
                if comp_loinc == "8480-6": # Systolic
                    parsed_vitals["bp_systolic"] = {"value": comp_val, "unit": comp_unit}
                elif comp_loinc == "8462-4": # Diastolic
                    parsed_vitals["bp_diastolic"] = {"value": comp_val, "unit": comp_unit}

    # Format to a consolidated state suitable for UI consumption
    return json.dumps(parsed_vitals)
