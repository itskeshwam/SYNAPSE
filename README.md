# SYNAPSE — Multi-Agent System with MCP and A2A

SYNAPSE is an automated, context-aware report generation system. It uses a multi-agent architecture to aggregate news, weather, financial data, and media assets into a unified daily briefing.

The system relies on:

- **Model Context Protocol (MCP)** for communication between agents and tool servers  
- **Agent-to-Agent (A2A)** coordination through a lightweight asynchronous messaging layer called **Post Office**

---

# Core Architecture

## Agents

### Contextualist Agent
Retrieves contextual signals by collecting:
- News headlines
- Weather data
- Foreign exchange rates

The agent transforms these inputs into a structured **context signal** used by downstream agents.

### Scout Agent
Acts as a **data aggregator**.

Responsibilities:
- Communicates with the Contextualist Agent
- Retrieves media assets from the Media Engine
- Combines all retrieved information into a single payload

### Publisher Agent
Processes the aggregated payload using an **OpenAI LLM**.

Responsibilities:
- Generate a neutral, professional journalistic report
- Convert structured payloads into readable narrative articles

---

# MCP Tool Servers

### World Data Server
Provides contextual world information.

Tools include:
- **News search** via NewsAPI
- **Weather retrieval** via OpenWeatherMap

### Finance Monitor Server
Handles financial context.

Features:
- Fetches available currency codes
- Retrieves FX conversion rates relative to **USD**

### Media Engine Server
Provides visual media.

Features:
- Searches high-quality images
- Uses the **Pexels API** to retrieve relevant assets

---

# Messaging Layer

### Post Office
A lightweight **JSON-based message hub** (`post_office.json`).

Purpose:
- Enables asynchronous communication between agents
- Supports decoupled A2A workflows
- Allows agents to **send**, **receive**, and **poll** messages

---

# Setup and Installation

## 1. Prerequisites

Ensure **Python** is installed.

You will also need API keys for:

- OpenAI
- NewsAPI
- OpenWeatherMap
- Pexels
- ExchangeRate-API

---

## 2. Environment Variables

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_key
NEWSAPI_KEY=your_newsapi_key
OPENWEATHER_API_KEY=your_openweather_key
PEXELS_API_KEY=your_pexels_key
EXCHANGE_RATE_API_KEY=your_exchangerate_key
```
## 3. Install Dependencies

Run the following command to install required packages:

```bash
pip install fastmcp streamlit openai requests python-dotenv
```

---

# Running the Project

Run each component in **separate terminal windows** to simulate a distributed environment.

---

## Step 1 — Start MCP Tool Servers

```bash
# Terminal 1 — World Data Server (Port 8001)
python synapse/mcp-servers/world-data/server.py

# Terminal 2 — Finance Monitor Server (Port 8002)
python synapse/mcp-servers/finance-monitor/server.py

# Terminal 3 — Media Engine Server (Port 8003)
python synapse/mcp-servers/media-engine/server.py
```

---

## Step 2 — Start Agents

```bash
# Terminal 4 — Contextualist Agent (Port 8000)
python synapse/agents/contextualist_agent/main.py

# Terminal 5 — Scout Agent (Port 8004)
python synapse/agents/scout_agent/main.py

# Terminal 6 — Publisher Agent (Port 8005)
python synapse/agents/publisher_agent/main.py
```

---

## Step 3 — Launch the UI

```bash
# Terminal 7 — Streamlit Frontend
streamlit run synapse/ui/app.py
```

---

# Usage

1. Enter a **Topic** in the Streamlit interface.

Example:

```
Semiconductor factory opening in Japan
```

2. The system automatically uses an LLM to identify the relevant **City**.

Example:

```
Tokyo
```

3. Click **Generate Report** to trigger the agent workflow.

4. The system generates:

- A professional journalistic article  
- Relevant imagery  
- The structured data payload used to generate the report

---

# System Flow

```
User Input
   ↓
Contextualist Agent
   ↓
Scout Agent
   ↓
Publisher Agent (LLM)
   ↓
Final Report + Images
```

---

# Project Structure

```
synapse/
│
├── agents/
│   ├── contextualist_agent/
│   ├── scout_agent/
│   └── publisher_agent/
│
├── mcp-servers/
│   ├── world-data/
│   ├── finance-monitor/
│   └── media-engine/
│
├── ui/
│   └── app.py
│
├── post_office.json
└── README.md
```

---

# Summary

SYNAPSE demonstrates how **MCP-powered tool servers**, **LLM-driven agents**, and **asynchronous agent messaging** can be combined to build a scalable automated reporting system that transforms global signals into coherent daily intelligence reports.
