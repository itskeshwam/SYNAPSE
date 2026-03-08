import streamlit as st
import asyncio
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastmcp import Client

load_dotenv()  # Load environment variables

# MCP agent URLs
SCOUT_URL = "http://localhost:8004/mcp"
PUBLISHER_URL = "http://localhost:8005/mcp"

# Fetch Groq API key from environment
api_key = os.getenv("GROQ_API_KEY")

# Pre-provided Groq/OpenAI client pointing to Groq's infrastructure
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Async helper to call MCP tools
async def call_tool(url, tool, params):
    async with Client(url) as client_mcp:
        res = await client_mcp.call_tool(tool, params)
        
        # FastMCP 3.1.0 natively stores structured returns in .data
        if hasattr(res, 'data') and res.data is not None:
            return res.data
            
        # Fallback: Parse stringified JSON from raw content block
        if hasattr(res, 'content') and res.content:
            try:
                import json
                return json.loads(res.content[0].text)
            except Exception:
                return {"error": "Unparseable response", "raw": res.content[0].text}
                
        return {}

def get_location_context(news_text: str) -> dict:
    """
    Extracts country and capital from a text string using Groq.
    """
    prompt = f"""
    Given the news text below, identify the primary country it is about.
    Return only a JSON object with the keys 'country' and 'capital'.
    If no country is mentioned, return US and its capital for both.

    Text: "{news_text}"
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"country": "US", "capital": "Washington"}

# Helper functions for UI
def run_scout(topic, city):
    return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))

def run_publisher(payload):
    return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))

def normalize_payload(payload):
    try:
        img = payload["media"]["images"][0]
        src = img.get("src")
        if isinstance(src, str):
            img["src"] = {"url": src, "type": "image"}
    except Exception:
        pass
    return payload

# Streamlit UI
st.set_page_config(page_title="SYNAPSE", layout="wide")
st.title("SYNAPSE - Multi-Agent Reporting")

topic = st.text_input("Topic", "Semiconductor factory opening in Japan")

# Get city context
location_data = get_location_context(topic)
city = location_data['capital']
st.info(f"Detected Context: {city}, {location_data['country']}")

if st.button("Generate Report"):
    with st.status("Agent Orchestration in progress..."):
        st.write("Scout Agent: Aggregating real-time signals...")
        scout_data = run_scout(topic, city)
        scout_data = normalize_payload(scout_data)

        st.write("Publisher Agent: Synthesizing final brief...")
        publisher_data = run_publisher(scout_data)

    st.subheader("Final Article")
    st.markdown(publisher_data.get("article", "No output generated."))

    try:
        image_url = scout_data["media"]["images"][0]["src"]["url"]
        if image_url:
            st.image(image_url, caption="Automated Media Asset", use_container_width=True)
    except Exception:
        pass

    with st.expander("View Raw Data Payload"):
        st.json(publisher_data.get("payload"))