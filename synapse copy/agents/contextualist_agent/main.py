# # /usercode/synapse/agents/contextualist_agent/main.py
import os
import asyncio
import json
from fastmcp import FastMCP, Client
from contextlib import AsyncExitStack
# from protocol.post_office import send_message, read_messages
from synapse.protocol.post_office import send_message, read_messages

mcp = FastMCP("Contextualist Agent")

WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"
FINANCE_URL = "http://0.0.0.0:8002/mcp"

@mcp.tool
async def contextualize(topic: str, city: str, task_id: str = "task-1"):
    async with AsyncExitStack() as stack:
        world_client = await stack.enter_async_context(Client(WORLD_DATA_URL))
        finance_client = await stack.enter_async_context(Client(FINANCE_URL))

        results = await asyncio.gather(
            world_client.call_tool("search_news", {"query": topic}),
            world_client.call_tool("get_weather", {"city": city}),
            finance_client.call_tool("get_fx_rate", {"location": city})
        )

        news, weather, fx = [r.data for r in results]

    signal = {
        "topic": topic,
        "news_headline": news.get("headline"),
        "location": {
            "city": city,
            "weather": f"{weather.get('temperature')}°C, {weather.get('description')}"
        },
        "financial_context": fx,
    }

    # send message to post office
    send_message({
        "sender": "contextualist",
        "recipient": "scout",
        "task_id": task_id,
        "status": "done",
        "payload": signal
    })

    return signal


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

















# import os
# import asyncio
# import json
# from fastmcp import FastMCP, Client
# from contextlib import AsyncExitStack

# mcp = FastMCP("Contextualist Agent")

# # MCP Endpoints
# WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"
# FINANCE_URL = "http://0.0.0.0:8002/mcp"

# @mcp.tool
# async def contextualize(topic: str, city: str) -> dict:
#     """
#     Combine news, weather, and FX rate into a context signal.
#     """
#     async with AsyncExitStack() as stack:
#         world_client = await stack.enter_async_context(Client(WORLD_DATA_URL))
#         finance_client = await stack.enter_async_context(Client(FINANCE_URL))

#         # Parallel calls
#         results = await asyncio.gather(
#             world_client.call_tool("search_news", {"query": topic}),
#             world_client.call_tool("get_weather", {"city": city}),
#             finance_client.call_tool("get_fx_rate", {"location": city})
#         )

#         news, weather, fx = [r.data for r in results]

#     signal = {
#         "topic": topic,
#         "location": {
#             "city": city,
#             "weather": f"{weather.get('temperature')}°C, {weather.get('description')}"
#         },
#         "financial_context": fx,
#         "news_headline": news.get("headline"),
#         "news_source": news.get("source"),
#         "news_url": news.get("url"),
#         "published_at": news.get("published_at")
#     }

#     print(json.dumps(signal, indent=2, ensure_ascii=False))
#     return signal


# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8000)







# import asyncio
# from fastmcp import Client
# from contextlib import AsyncExitStack
# import json

# # Define your endpoints
# WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"
# FINANCE_URL = "http://0.0.0.0:8002/mcp"


# async def contextualize(topic: str, city: str):
#     async with AsyncExitStack() as stack:
#         world_client = await stack.enter_async_context(Client(WORLD_DATA_URL))
#         finance_client = await stack.enter_async_context(Client(FINANCE_URL))

#         # # 1. DYNAMIC LOOKUP: Get currency code from the country/city name
#         # map_res = await world_client.call_tool("get_currency_code", {"location": city})
#         # # Use JPY as fallback if the API fails
#         # currency_code = map_res.data.get("currency_code", "JPY") 

#         # 2. PARALLEL CALLS: Fetch everything else using the discovered code
#         results = await asyncio.gather(
#             world_client.call_tool("search_news", {"query": topic}),
#             world_client.call_tool("get_weather", {"city": city}),
#             finance_client.call_tool("get_fx_rate", {"location": city})
#             # finance_client.call_tool("get_fx_rate", {"base": currency_code})
#         )

#         # 3. UNWRAP DATA
#         news, weather, fx = [r.data for r in results]

#     # 4. FINAL SIGNAL
#     signal = {
#         "topic": topic,
#         "location_context": {
#             "city": city,
#             "weather": f"{weather.get('temperature')}°C, {weather.get('description')}"
#         },
#         "financial_context": fx,
#         "news_headline": news.get("headline")
#     }

#     print(json.dumps(signal, indent=2, ensure_ascii=False))
#     return signal


# if __name__ == "__main__":
#     # The dictionary keys here must match the function arguments exactly
#     params = {
#         "topic": "Pakistan tech news",
#         "city": "Islamabad"
#     }
#     asyncio.run(contextualize(**params))

