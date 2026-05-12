<div align="center">

# H.E.R.O.

### Health Entity Rendering Orchestrator

**An intelligent A2A Agent and MCP Server that transforms raw FHIR healthcare records into actionable clinical insights**

[![MCP Protocol](https://img.shields.io/badge/MCP-SSE%20Transport-00B4D8?style=for-the-badge)](https://modelcontextprotocol.io)
[![A2A Protocol](https://img.shields.io/badge/A2A-Agent_to_Agent-7B2FF7?style=for-the-badge)](https://google.github.io/A2A/)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4%20Compliant-E63946?style=for-the-badge)](https://hl7.org/fhir/)
[![Platform](https://img.shields.io/badge/Prompt_Opinion-Integrated-1A1A2E?style=for-the-badge)](https://promptopinion.com)

---

*Built for the **Agents Assemble: The Healthcare AI Endgame Challenge** by Prompt Opinion*

</div>

---

## The Problem

Healthcare data is fragmented, deeply nested, and impossible to interpret at a glance. A single patient's FHIR record can contain hundreds of resources across observations, conditions, medications, and encounters — buried in JSON structures that no clinician has time to parse manually.

**The result?** Critical patterns get missed. Cross-condition interactions go unnoticed. And the gap between raw EHR data and clinical action keeps growing.

## The Solution

**H.E.R.O.** bridges that gap by orchestrating specialized AI agents that ingest raw FHIR data and deliver structured, actionable clinical intelligence — mapping conditions to body systems, flagging abnormal vitals, and surfacing risk patterns instantly.

> HERO bridges the gap between raw healthcare data and actionable clinical insights by translating complex FHIR records into structured clinical analysis. By orchestrating specialized MCP tools, it transforms a static patient history into a real-time clinical command center.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PROMPT OPINION PLATFORM                       │
│                                                                      │
│  ┌─────────────┐    ┌──────────────────────────────────────────┐    │
│  │  Patient DB  │───▶│         HERO A2A Agent (Layer B)         │    │
│  │  (FHIR R4)   │    │                                          │    │
│  └─────────────┘    │  • Structured clinical analysis           │    │
│                      │  • Condition-to-body-system mapping       │    │
│                      │  • Vital sign assessment & flagging       │    │
│                      │  • Cross-condition risk identification    │    │
│                      └────────────────┬─────────────────────────┘    │
│                                       │                              │
│                                       │ MCP Protocol (SSE)           │
│                                       │                              │
│                      ┌────────────────▼─────────────────────────┐    │
│                      │      FHIR MCP Server (Layer A)            │    │
│                      │                                           │    │
│                      │  ┌─────────────────────────────────────┐  │    │
│                      │  │  patient_vitals_tool                 │  │    │
│                      │  │  → HR, BP, SpO2, RR parsing          │  │    │
│                      │  │  → LOINC code matching               │  │    │
│                      │  ├─────────────────────────────────────┤  │    │
│                      │  │  patient_conditions_tool             │  │    │
│                      │  │  → Active SNOMED/ICD-10 extraction   │  │    │
│                      │  │  → Clinical status filtering         │  │    │
│                      │  ├─────────────────────────────────────┤  │    │
│                      │  │  SHARP Context Handler               │  │    │
│                      │  │  → Secure token propagation          │  │    │
│                      │  │  → Patient ID resolution             │  │    │
│                      │  └─────────────────────────────────────┘  │    │
│                      └───────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
H.E.R.O./
├── fhir-mcp-server/                # Layer A — MCP Server (Python)
│   ├── server.py                    # SSE transport server (Starlette + Uvicorn)
│   ├── patient_vitals_tool.py       # FHIR Observation parser (LOINC-coded vitals)
│   ├── patient_conditions_tool.py   # FHIR Condition parser (active dx filter)
│   └── fhir_context.py             # SHARP context handler (token propagation)
│
├── fhir-a2a-agent/                  # Layer B — A2A Orchestrator Agent (Python)
│   └── orchestrator.py             # Clinical twin agent + state broadcaster
│
├── generate_patient_report.py       # Demo patient report generator (PDF)
├── Priya_Sharma_Clinical_Report.pdf # Sample clinical discharge summary
└── README.md
```

---

## Key Features

### Layer A — FHIR MCP Server

The MCP Server exposes healthcare data tools over the **Model Context Protocol** using HTTP/SSE transport, allowing any MCP-compatible agent to query patient records.

| Component | Description |
|---|---|
| **Transport** | HTTP/SSE — `GET /sse` (event stream) · `POST /messages/` (JSON-RPC) |
| **Health Check** | `GET /` returns server status JSON |
| **Security** | DNS rebinding protection disabled for tunnel compatibility |

**Tools Exposed:**

- **`patient_vitals_tool`** — Parses FHIR R4 `Observation` bundles. Extracts Heart Rate, Blood Pressure (Systolic & Diastolic), and Oxygen Saturation (SpO2) by matching LOINC codes (`8867-4`, `8480-6`, `8462-4`, `2708-6`). Returns normalized `{ value, unit }` objects.

- **`patient_conditions_tool`** — Filters FHIR R4 `Condition` bundles for entries where `clinicalStatus.coding[0].code === 'active'`. Returns a clean list of condition display names from `code.coding[0].display`.

**SHARP Context Handler:**
- Implements the Secure Healthcare Agent Request Protocol specification
- Extracts patient IDs and FHIR tokens propagated through multi-agent call chains
- Supports both environment variable injection and MCP request metadata extraction

### Layer B — A2A Orchestrator Agent

The orchestrator agent follows **Google ADK Agent-to-Agent** architecture patterns. It consumes parsed FHIR data from Layer A and produces structured clinical analysis.

**Capabilities:**
- Receives parsed FHIR data from MCP tools
- Maps clinical conditions to anatomical body systems
- Generates consolidated clinical state objects
- Broadcasts real-time state updates via WebSocket

**Condition → Body System Mapping:**

| Condition Pattern | Body System |
|---|---|
| Asthma, COPD, Bronchitis, Pneumonia | Lungs (Respiratory) |
| Hypertension, Coronary Disease, Arrhythmia | Heart (Cardiovascular) |
| Diabetes, GI Disorders | Abdomen (Gastrointestinal) |
| Migraines, Neurological Conditions | Head (Neurological) |
| Arthritis, Musculoskeletal | Joints/Limbs |
| Anemia, Autoimmune, Allergic | Systemic |

---

## Hackathon Compliance

| Requirement | Implementation | Status |
|---|---|---|
| **MCP Server** | `fhir-mcp-server/server.py` — SSE transport, 2 FHIR tools | ✅ |
| **A2A Agent** | `fhir-a2a-agent/orchestrator.py` — Google ADK orchestrator | ✅ |
| **FHIR R4 Data** | LOINC-coded vitals + SNOMED/ICD-10 condition parsing | ✅ |
| **SHARP Spec** | `fhir_context.py` — Secure token propagation handler | ✅ |
| **Prompt Opinion Integration** | MCP Server registered via SSE, Agent configured on platform | ✅ |

---

## Quick Start

### Prerequisites
- Python 3.11+
- `pip install mcp uvicorn starlette websockets`

### 1. Start the MCP Server (Layer A)
```bash
cd fhir-mcp-server
pip install mcp uvicorn starlette
python server.py
```
```
Server runs on http://0.0.0.0:8000
  GET  /       → Health check (JSON)
  GET  /sse    → SSE event stream
  POST /messages/ → JSON-RPC messages
```

### 2. Start the A2A Orchestrator (Layer B)
```bash
cd fhir-a2a-agent
pip install websockets
python orchestrator.py
```
```
WebSocket server on ws://localhost:8765
```

### 3. Expose via ngrok (for Prompt Opinion)
```bash
ngrok http 8000
# Use the generated HTTPS URL as the MCP Server endpoint in Prompt Opinion
```

### 4. Register on Prompt Opinion
1. Navigate to **Configuration → MCP Servers**
2. Set **Endpoint** to your ngrok HTTPS URL
3. Set **Transport Type** to `SSE`
4. Set **Authentication** to `No Authentication (Open)`
5. Click **Continue** — tools will be auto-discovered

---

## HERO Agent System Prompt

The A2A agent on Prompt Opinion uses this system prompt to drive clinical analysis:

```
You are HERO (Health Evidence & Risk Observer), an advanced Clinical Digital Twin AI agent.
Your purpose is to analyze patient clinical data from FHIR-standard electronic health records
and produce structured clinical intelligence.

CORE BEHAVIOR:
1. Always call patient_conditions_tool and patient_vitals_tool when patient context is available
2. Present structured analysis: Patient Summary → Active Conditions → Vital Signs → Body System Mapping → Risk Flags → Recommendations
3. Map conditions to anatomical regions (Asthma → Lungs, Hypertension → Heart, etc.)
4. Cite LOINC codes for vitals and SNOMED/ICD-10 codes for conditions
5. Flag critical values with ⚠️
```

---

## Demo Patient: Priya Sharma

The included clinical report (`Priya_Sharma_Clinical_Report.pdf`) is a professional discharge summary for testing:

| Parameter | Value | Flag |
|---|---|---|
| **Active Conditions** | Mild Persistent Asthma (J45.30), Essential Hypertension Stage 1 (I10), Allergic Rhinitis (J30.1) | — |
| **Heart Rate** | 112 → 78 bpm (admission → discharge) | HIGH → Normal |
| **Blood Pressure** | 148/94 → 126/82 mmHg | HIGH → Borderline |
| **SpO2** | 91% → 97% | LOW → Normal |
| **Serum IgE** | 485 IU/mL (ref: <100) | HIGH |

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| MCP Server | Python, Starlette, Uvicorn, `mcp` SDK | FHIR tool hosting over SSE |
| A2A Agent | Python, Google ADK concepts, WebSockets | Clinical orchestration |
| Tunnel | ngrok | External HTTPS exposure |
| Platform | Prompt Opinion | Agent + MCP registration |
| Data Standard | HL7 FHIR R4, LOINC, SNOMED CT, ICD-10 | Healthcare interoperability |

---

## Team

Built by **Ayush Shukla** for the **Agents Assemble: The Healthcare AI Endgame Challenge** hackathon by Prompt Opinion.

---

<div align="center">

**H.E.R.O.** — *Because healthcare data deserves to be understood, not just stored.*

</div>
