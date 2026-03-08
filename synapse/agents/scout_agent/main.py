import os
import asyncio
from fastmcp import FastMCP, Client
from contextlib import AsyncExitStack
from synapse.protocol.post_office import send_message

mcp = FastMCP("Scout Agent")

CONTEXTUALIST_URL = "http://127.0.0.1:8000/mcp"
MEDIA_ENGINE_URL = "http://127.0.0.1:8003/mcp"

@mcp.tool
async def scout(topic: str, city: str, task_id: str = "task-1"):
    async with AsyncExitStack() as stack:
        context_client = await stack.enter_async_context(Client(CONTEXTUALIST_URL))
        media_client = await stack.enter_async_context(Client(MEDIA_ENGINE_URL))

        # Fix: Call "search_images" instead of "get_media"
        context_result = await context_client.call_tool("contextualize", {"topic": topic, "city": city})
        media_result = await media_client.call_tool("search_images", {"query": topic})

    # Fix: Extract .data from the CallToolResult objects
    payload = {
        "context": context_result.data if hasattr(context_result, 'data') else context_result,
        "media": media_result.data if hasattr(media_result, 'data') else media_result
    }

    send_message({
        "sender": "scout",
        "recipient": "publisher",
        "task_id": task_id,
        "status": "ready",
        "payload": payload
    })

    return payload

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8004)
