<div align="center">

# H.E.R.O.

### Health Entity Rendering Orchestrator

**Transforming raw FHIR healthcare records into an interactive 3D Clinical Digital Twin**

[![MCP Protocol](https://img.shields.io/badge/MCP-SSE%20Transport-00B4D8?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+PHBhdGggZD0iTTEyIDJMMiA3bDEwIDUgMTAtNS0xMC01ek0yIDE3bDEwIDUgMTAtNS0xMC01LTEwIDV6TTIgMTJsMTAgNSAxMC01LTEwLTUtMTAgNXoiLz48L3N2Zz4=)](https://modelcontextprotocol.io)
[![A2A Protocol](https://img.shields.io/badge/A2A-Agent_to_Agent-7B2FF7?style=for-the-badge)](https://google.github.io/A2A/)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4%20Compliant-E63946?style=for-the-badge)](https://hl7.org/fhir/)
[![Platform](https://img.shields.io/badge/Prompt_Opinion-Integrated-1A1A2E?style=for-the-badge)](https://promptopinion.com)
[![Three.js](https://img.shields.io/badge/Three.js-3D_Visualization-000000?style=for-the-badge&logo=three.js)](https://threejs.org)

---

*Built for the **Agents Assemble: The Healthcare AI Endgame Challenge** by Prompt Opinion*

</div>

---

## The Problem

Healthcare data is fragmented, deeply nested, and impossible to interpret at a glance. A single patient's FHIR record can contain hundreds of resources across observations, conditions, medications, and encounters — buried in JSON structures that no clinician has time to parse manually.

**The result?** Critical patterns get missed. Cross-condition interactions go unnoticed. And the gap between raw EHR data and clinical action keeps growing.

## The Solution

**H.E.R.O.** bridges that gap by orchestrating specialized AI agents that ingest raw FHIR data and render it as a real-time, interactive **3D Clinical Digital Twin** — a visual command center where conditions light up on a human body model, vitals pulse in real-time, and clinical intelligence is delivered instantly.

> HERO bridges the gap between raw healthcare data and actionable clinical insights by translating complex FHIR records into an interactive 3D digital twin. By orchestrating specialized MCP tools, it transforms a static patient history into a real-time, visual command center.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PROMPT OPINION PLATFORM                       │
│  ┌─────────────┐    ┌──────────────────────────────────────────┐    │
│  │  Patient DB  │───▶│         HERO A2A Agent (Layer B)         │    │
│  │  (FHIR R4)   │    │  • Clinical analysis & triage            │    │
│  └─────────────┘    │  • Condition-to-anatomy mapping           │    │
│                      │  • Risk flag generation                   │    │
│                      └────────────────┬─────────────────────────┘    │
│                                       │ MCP Protocol (SSE)           │
│                      ┌────────────────▼─────────────────────────┐    │
│                      │      FHIR MCP Server (Layer A)            │    │
│                      │  ┌─────────────────────────────────────┐  │    │
│                      │  │  patient_vitals_tool                 │  │    │
│                      │  │  → HR, BP, SpO2, RR parsing          │  │    │
│                      │  ├─────────────────────────────────────┤  │    │
│                      │  │  patient_conditions_tool             │  │    │
│                      │  │  → Active SNOMED/ICD-10 extraction   │  │    │
│                      │  ├─────────────────────────────────────┤  │    │
│                      │  │  SHARP Context Handler               │  │    │
│                      │  │  → Secure token propagation          │  │    │
│                      │  └─────────────────────────────────────┘  │    │
│                      └───────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                            WebSocket (ws://8765)
                                    │
┌───────────────────────────────────▼──────────────────────────────────┐
│                     3D DIGITAL TWIN UI (Layer C)                     │
│  ┌──────────────────────────────┐  ┌─────────────────────────────┐  │
│  │    Three.js / R3F Canvas     │  │     Clinical Data Panel     │  │
│  │  • Procedural human body     │  │  • Real-time vitals         │  │
│  │  • Dynamic neon highlights   │  │  • Active conditions list   │  │
│  │  • Orbit camera controls     │  │  • Glassmorphism UI         │  │
│  └──────────────────────────────┘  └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
H.E.R.O./
├── fhir-mcp-server/          # Layer A — MCP Server (Python)
│   ├── server.py              # SSE transport server (Starlette + Uvicorn)
│   ├── patient_vitals_tool.py # FHIR Observation parser (LOINC-coded vitals)
│   ├── patient_conditions_tool.py  # FHIR Condition parser (active dx filter)
│   └── fhir_context.py        # SHARP context handler (token propagation)
│
├── fhir-a2a-agent/            # Layer B — A2A Orchestrator Agent (Python)
│   └── orchestrator.py        # Clinical twin agent + WebSocket broadcaster
│
├── fhir-3d-twin/              # Layer C — 3D Digital Twin UI (React)
│   ├── src/
│   │   ├── App.jsx            # Main layout — canvas + clinical panel
│   │   ├── components/
│   │   │   ├── HumanBody.jsx  # Procedural 3D wireframe human body
│   │   │   └── DataPanel.jsx  # Real-time vitals & conditions display
│   │   └── App.css            # Dark mode clinical control center styles
│   └── package.json
│
├── generate_patient_report.py  # Demo patient report generator (PDF)
├── Priya_Sharma_Clinical_Report.pdf  # Sample clinical report
└── README.md
```

---

## Key Features

### Layer A — FHIR MCP Server
- **Protocol**: Model Context Protocol over HTTP/SSE transport
- **Endpoints**: `GET /sse` (event stream) · `POST /messages/` (JSON-RPC)
- **Tools Exposed**:
  - `patient_vitals_tool` — Parses FHIR Observation bundles, extracts Heart Rate, Blood Pressure (Systolic/Diastolic), and SpO2 using LOINC code matching
  - `patient_conditions_tool` — Filters FHIR Condition bundles for `clinicalStatus.coding[0].code === 'active'`, returns clean condition display names
- **Security**: SHARP (Secure Healthcare Agent Request Protocol) context handler for token propagation without bespoke token vaults

### Layer B — A2A Orchestrator Agent
- **Framework**: Google ADK-compatible Agent-to-Agent architecture
- **Role**: Receives parsed FHIR data from MCP tools, maps conditions to anatomical regions, generates consolidated UI state
- **Output**: Real-time WebSocket broadcast of `{ vitals, conditions, highlighted_meshes }` to the frontend
- **Condition → Anatomy Mapping**:
  | Condition | Body System |
  |---|---|
  | Asthma, COPD, Bronchitis | Lungs (Respiratory) |
  | Hypertension, Heart Disease | Heart (Cardiovascular) |

### Layer C — 3D Digital Twin UI
- **Stack**: React + Three.js (React Three Fiber) + Tailwind CSS
- **Aesthetic**: Dark clinical control center with glassmorphism panels
- **3D Canvas**: Procedural wireframe human body built from Three.js primitives with dynamic neon highlights that activate based on detected conditions
- **Real-time**: WebSocket listener auto-updates vitals and condition highlights

---

## Hackathon Compliance

| Requirement | Implementation | Status |
|---|---|---|
| **MCP Server** | `fhir-mcp-server/server.py` — SSE transport, 2 FHIR tools | ✅ |
| **A2A Agent** | `fhir-a2a-agent/orchestrator.py` — Google ADK orchestrator | ✅ |
| **FHIR R4 Data** | LOINC-coded vitals + SNOMED/ICD-10 conditions parsing | ✅ |
| **SHARP Spec** | `fhir_context.py` — Token propagation handler | ✅ |
| **Prompt Opinion Integration** | MCP Server registered via SSE, Agent configured on platform | ✅ |
| **Interactive UI** | 3D Digital Twin with real-time WebSocket updates | ✅ |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- `pip install mcp uvicorn starlette websockets`

### 1. Start the MCP Server (Layer A)
```bash
cd fhir-mcp-server
pip install mcp uvicorn starlette
python server.py
# Server runs on http://0.0.0.0:8000
# SSE endpoint: GET /sse
# Messages:     POST /messages/
```

### 2. Start the A2A Orchestrator (Layer B)
```bash
cd fhir-a2a-agent
pip install websockets
python orchestrator.py
# WebSocket server on ws://localhost:8765
```

### 3. Start the 3D Digital Twin UI (Layer C)
```bash
cd fhir-3d-twin
npm install
npm run dev
# React app on http://localhost:5173
```

### 4. Expose via ngrok (for Prompt Opinion)
```bash
ngrok http 8000
# Use the generated HTTPS URL as the MCP Server endpoint in Prompt Opinion
```

---

## Demo Patient: Priya Sharma

The included clinical report (`Priya_Sharma_Clinical_Report.pdf`) contains a complete discharge summary for a 24-year-old female patient with:

| Parameter | Value | Flag |
|---|---|---|
| **Active Conditions** | Mild Persistent Asthma (J45.30), Essential Hypertension Stage 1 (I10), Allergic Rhinitis (J30.1) | — |
| **Heart Rate** | 112 → 78 bpm (admission → discharge) | HIGH → Normal |
| **Blood Pressure** | 148/94 → 126/82 mmHg | HIGH → Borderline |
| **SpO2** | 91% → 97% | LOW → Normal |
| **Serum IgE** | 485 IU/mL (ref: <100) | HIGH |

This data directly maps to the 3D Digital Twin — **Lungs** glow red (Asthma), **Heart** pulses with alert coloring (Hypertension).

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| MCP Server | Python, Starlette, Uvicorn, `mcp` SDK | FHIR tool hosting over SSE |
| A2A Agent | Python, Google ADK concepts, WebSockets | Clinical orchestration |
| 3D Frontend | React, Three.js, React Three Fiber, Tailwind CSS | Interactive visualization |
| Tunnel | ngrok | External HTTPS exposure |
| Platform | Prompt Opinion | Agent + MCP registration |
| Data Standard | HL7 FHIR R4, LOINC, SNOMED CT, ICD-10 | Healthcare interoperability |

---

## Team

Built by **Ayush Shukla** for the **Agents Assemble: The Healthcare AI Endgame Challenge** hackathon by Prompt Opinion.

---

<div align="center">

**H.E.R.O.** — *Because healthcare data deserves to be seen, not just stored.*

</div>
