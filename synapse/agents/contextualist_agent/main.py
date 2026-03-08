import os
import asyncio
import json
from fastmcp import FastMCP, Client
from contextlib import AsyncExitStack
from synapse.protocol.post_office import send_message

mcp = FastMCP("Contextualist Agent")

WORLD_DATA_URL = "http://localhost:8001/mcp"
FINANCE_URL = "http://localhost:8002/mcp"

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