@echo off
set PYTHONPATH=.

:: 1. Start Tool Servers (The Data Providers)
start cmd /k "title World Data && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/mcp-servers/world-data/server.py"
start cmd /k "title Finance Monitor && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/mcp-servers/finance-monitor/server.py"
start cmd /k "title Media Engine && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/mcp-servers/media-engine/server.py"

:: Wait for tools to boot up
timeout /t 8

:: 2. Start Agents (The Logic Layer)
start cmd /k "title Contextualist Agent && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/agents/contextualist_agent/main.py"
start cmd /k "title Scout Agent && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/agents/scout_agent/main.py"
start cmd /k "title Publisher Agent && call venv\Scripts\activate && set PYTHONPATH=. && python synapse/agents/publisher_agent/main.py"

:: 3. Start UI
start cmd /k "title Synapse UI && call venv\Scripts\activate && set PYTHONPATH=. && streamlit run synapse/ui/app.py"