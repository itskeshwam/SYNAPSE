import streamlit as st
import asyncio
from fastmcp import Client
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()  # This loads the variables from .env into the environment

SCOUT_URL = "http://0.0.0.0:8004/mcp"
PUBLISHER_URL = "http://0.0.0.0:8005/mcp"


# 1. Fetch the key from the environment using os.getenv
api_key = os.getenv("OPENAI_API_KEY")


async def call_tool(url, tool, params):
    async with Client(url) as client:
        res = await client.call_tool(tool, params)
        return res.data


client = OpenAI(api_key=api_key)

def get_location_context(news_text: str) -> dict:
    """
    Extracts country and capital from a text string using an LLM.
    """
    prompt = f"""
    Given the news text below, identify the primary country it is about.
    Return only a JSON object with the keys 'country' and 'capital'.
    If no country is mentioned, return US and its capital for both.

    Text: "{news_text}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Or any other LLM like Gemini
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" } # Ensures clean JSON output
    )

    return json.loads(response.choices[0].message.content)

# # Example Usage:
# news = "Heavy rain causes flooding in streets across Tokyo."
# result = get_location_context(news)
# print(result) 
# # Output: {'country': 'Japan', 'capital': 'Tokyo'}

def run_scout(topic, city):
    return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))


def run_publisher(payload):
    return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))


def normalize_payload(payload):
    """
    Ensures image src is a valid JSON object (dict).
    """
    try:
        img = payload["media"]["images"][0]
        src = img.get("src")

        # If src is a string, convert to dict
        if isinstance(src, str):
            img["src"] = {"url": src, "type": "image"}

        # If src is missing, set a default dict
        if src is None:
            img["src"] = {"url": "", "type": "image"}

    except Exception:
        pass

    return payload


st.title("SYNAPSE - Context Aware Reports")

topic = st.text_input("Topic", "Semiconductor factory opening in Japan")
# print(get_location_context(topic)['capital'])
city = get_location_context(topic)['capital'] # st.text_input("City", "Tokyo")

if st.button("Generate Report"):
    st.write("Running Scout...")
    scout_data = run_scout(topic, city)

    # Normalize before sending to publisher
    scout_data = normalize_payload(scout_data)

    st.write("Running Publisher...")
    publisher_data = run_publisher(scout_data)

    # Render Article
    st.subheader("Final Article")
    with st.expander("Read full article"):
        st.markdown(publisher_data.get("article", "No output"), unsafe_allow_html=True)

    # Render Image (guaranteed)
    image_url = scout_data["media"]["images"][0]["src"]["url"]
    if image_url:
        st.image(image_url, caption="Related Image", width="stretch")

    # Optional: Payload
    st.subheader("Payload")
    st.json(publisher_data.get("payload"))

    # Show signal only if valid
    signal = publisher_data.get("signal")
    if isinstance(signal, dict) and "ERROR" not in signal:
        st.subheader("Full Signal")
        st.json(signal)
    else:
        st.write("Signal is invalid or contains errors.")












# import streamlit as st
# import asyncio
# from fastmcp import Client

# SCOUT_URL = "http://0.0.0.0:8004/mcp"
# PUBLISHER_URL = "http://0.0.0.0:8005/mcp"


# async def call_tool(url, tool, params):
#     async with Client(url) as client:
#         res = await client.call_tool(tool, params)
#         return res.data


# def run_scout(topic, city):
#     return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))


# def run_publisher(payload):
#     return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))


# st.title("SYNAPSE - Context Aware Reports")

# topic = st.text_input("Topic", "Semiconductor factory opening in Japan")
# city = st.text_input("City", "Tokyo")

# if st.button("Generate Report"):
#     st.write("Running Scout...")
#     scout_data = run_scout(topic, city)

#     st.write("Running Publisher...")
#     publisher_data = run_publisher(scout_data)

#     # Article rendering inside Expander
#     st.subheader("Final Article")
#     with st.expander("Read full article"):
#         st.markdown(publisher_data.get("article", "No output"))

#     # Payload & Signal (optional)
#     st.subheader("Payload")
#     st.json(publisher_data.get("payload"))

#     st.subheader("Full Signal")
#     st.json(publisher_data.get("signal"))











# import streamlit as st
# import asyncio
# from fastmcp import Client

# SCOUT_URL = "http://0.0.0.0:8004/mcp"
# PUBLISHER_URL = "http://0.0.0.0:8005/mcp"


# async def call_tool(url, tool, params):
#     async with Client(url) as client:
#         res = await client.call_tool(tool, params)
#         return res.data


# def run_scout(topic, city):
#     return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))


# # def run_publisher(signal):
# #     return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"signal": signal}))
# def run_publisher(payload):
#     return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))


# st.title("SYNAPSE - Context Aware Reports")

# topic = st.text_input("Topic", "Semiconductor factory opening in Japan")
# city = st.text_input("City", "Tokyo")

# if st.button("Generate Report"):
#     st.write("Running Scout...")
#     scout_data = run_scout(topic, city)

#     st.write("Running Publisher...")
#     publisher_data = run_publisher(scout_data)
#     print(publisher_data)

#     st.subheader("Final Report (Markdown)")
#     # st.code(publisher_data.get("markdown", "No output"))

#     # st.subheader("Full Signal")
#     # st.json(publisher_data.get("signal"))
#     st.code(publisher_data.get("article", "No output"))

#     st.subheader("Full Output")
#     st.json(publisher_data)







# PROBABLY THE WRONG ONE
# import streamlit as st
# import asyncio
# from fastmcp import Client
# from contextlib import AsyncExitStack


# WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"
# FINANCE_URL = "http://0.0.0.0:8002/mcp"
# MEDIA_URL = "http://0.0.0.0:8003/mcp"
# PUBLISHER_URL = "http://0.0.0.0:8004/mcp"


# async def fetch_all(topic: str, city: str):
#     async with AsyncExitStack() as stack:
#         world_client = await stack.enter_async_context(Client(WORLD_DATA_URL))
#         finance_client = await stack.enter_async_context(Client(FINANCE_URL))
#         media_client = await stack.enter_async_context(Client(MEDIA_URL))
#         publisher_client = await stack.enter_async_context(Client(PUBLISHER_URL))

#         # Parallel fetch
#         results = await asyncio.gather(
#             world_client.call_tool("search_news", {"query": topic}),
#             world_client.call_tool("get_weather", {"city": city}),
#             finance_client.call_tool("get_fx_rate", {"location": city}),
#             media_client.call_tool("search_images", {"query": topic, "per_page": 1})
#         )

#         news, weather, fx, images = [r.data for r in results]

#         payload = {
#             "topic": topic,
#             "location_context": {
#                 "city": city,
#                 "weather": f"{weather.get('temperature')}°C, {weather.get('description')}"
#             },
#             "financial_context": fx,
#             "news_headline": news.get("headline"),
#             "image_url": images.get("images", [{}])[0].get("src")
#         }

#         # Call Publisher
#         publish_result = await publisher_client.call_tool("publish_brief", {"payload": payload})
#         article = publish_result.data.get("article")

#         return payload, article


# def main():
#     st.title("Daily Brief Generator")

#     topic = st.text_input("Topic", "Semiconductor factory opening in Japan")
#     city = st.text_input("City", "Tokyo")

#     if st.button("Generate Daily Brief"):
#         payload, article = asyncio.run(fetch_all(topic, city))

#         st.markdown("## Payload")
#         st.json(payload)

#         st.markdown("## Article")
#         st.write(article)


# if __name__ == "__main__":
#     main()




# import streamlit as st
# import asyncio
# from fastmcp import Client

# SCOUT_URL = "http://0.0.0.0:8004/mcp"
# PUBLISHER_URL = "http://0.0.0.0:8005/mcp"

# async def call_tool(url, tool, params):
#     async with Client(url) as client:
#         res = await client.call_tool(tool, params)
#         return res.data

# def run_scout(topic, city):
#     return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))

# def run_publisher(task_id="task-1"):
#     return asyncio.run(call_tool(PUBLISHER_URL, "publish", {"task_id": task_id}))

# st.title("SYNAPSE - Context Aware Reports")

# topic = st.text_input("Topic", "Semiconductor factory opening in Japan")
# city = st.text_input("City", "Tokyo")

# if st.button("Generate Report"):
#     st.write("Running Scout...")
#     scout_data = run_scout(topic, city)

#     st.write("Running Publisher...")
#     publisher_data = run_publisher("task-1")

#     st.subheader("Final Report (Markdown)")
#     st.code(publisher_data.get("markdown", "No output"))

#     st.subheader("Full Signal")
#     st.json(publisher_data.get("signal"))
