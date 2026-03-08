# Task 6: Build Scout Agent to Aggregate Signals
import asyncio
import json
import time
from fastmcp import FastMCP, Client
from contextlib import AsyncExitStack
from synapse.protocol.post_office import send_message, read_messages, clear_messages

# Initialize the MCP server for the Scout agent
mcp = FastMCP("Scout Agent")

# MCP endpoints for downstream agents
CONTEXTUALIST_URL = "http://0.0.0.0:8000/mcp"
MEDIA_URL = "http://0.0.0.0:8003/mcp"


def wait_for_response(task_id: str, timeout: int = 10):
    """
    Poll the post office for a response matching the given task ID.
    """
    start = time.time()
    while time.time() - start < timeout:
        messages = read_messages()
        for msg in messages:
            if msg.get("task_id") == task_id and msg.get("recipient") == "scout":
                return msg
        time.sleep(0.5)
    return None


@mcp.tool
async def scout(topic: str, city: str, task_id: str = "task-1"):
    """
    Aggregate contextual and media signals for a given topic and city.
    """
    # Clear old messages to avoid mixing responses
    clear_messages()

    # Manage multiple MCP clients safely
    async with AsyncExitStack() as stack:
        # Connect to the Contextualist MCP server
        contextualist_client = await stack.enter_async_context(
            Client(CONTEXTUALIST_URL)
        )
        
        # Connect to the Media Engine MCP server
        media_client = await stack.enter_async_context(
            Client(MEDIA_URL)
        )

        # send request to contextualist
        await contextualist_client.call_tool(
            "contextualize", 
            {
                "topic": topic,
                "city": city,
                "task_id": task_id
            }
        )

        # Wait for the contextualist response via the post office
        response = wait_for_response(task_id)
        context = response["payload"]

        # Fetch related media assets
        media_res = await media_client.call_tool(
            "search_images", 
            {
                "query": topic, 
                "per_page": 1
            }
        )
        media = media_res.data

    # Combine all signals into one final object
    final_signal = {
        "topic": topic,
        "location": city,
        "context": context,
        "media": media
    }

    # Send final signal to publisher via post office
    send_message({
        "sender": "scout",
        "recipient": "publisher",
        "task_id": task_id,
        "status": "done",
        "payload": final_signal
    })

    # Log the final signal for debugging and visibility
    print(final_signal)

    return final_signal


if __name__ == "__main__":
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=8004
    )






# import asyncio
# import json
# import time
# from fastmcp import FastMCP, Client
# from contextlib import AsyncExitStack
# from protocol.post_office import send_message, read_messages, clear_messages

# mcp = FastMCP("Scout Agent")

# CONTEXTUALIST_URL = "http://0.0.0.0:8000/mcp"
# MEDIA_URL = "http://0.0.0.0:8003/mcp"

# def wait_for_response(task_id: str, timeout: int = 10):
#     start = time.time()
#     while time.time() - start < timeout:
#         messages = read_messages()
#         for msg in messages:
#             if msg.get("task_id") == task_id and msg.get("recipient") == "scout":
#                 return msg
#         time.sleep(0.5)
#     return None

# @mcp.tool
# async def scout(topic: str, city: str, task_id: str = "task-1"):
#     # clear post office for clean run
#     clear_messages()

#     async with AsyncExitStack() as stack:
#         contextualist_client = await stack.enter_async_context(Client(CONTEXTUALIST_URL))
#         media_client = await stack.enter_async_context(Client(MEDIA_URL))

#         # send request to contextualist
#         await contextualist_client.call_tool("contextualize", {
#             "topic": topic,
#             "city": city,
#             "task_id": task_id
#         })

#         # wait for contextualist response
#         response = wait_for_response(task_id)
#         context = response["payload"]

#         # get media
#         media_res = await media_client.call_tool("search_images", {"query": topic, "per_page": 1})
#         media = media_res.data

#     final_signal = {
#         "topic": topic,
#         "location": city,
#         "context": context,
#         "media": media
#     }

#     return final_signal


# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8004)












# import asyncio
# from fastmcp import Client
# from contextlib import AsyncExitStack
# import json

# # Endpoints
# CONTEXTUALIST_URL = "http://0.0.0.0:8000/mcp"  # Update if needed
# WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"
# FINANCE_URL = "http://0.0.0.0:8002/mcp"
# MEDIA_URL = "http://0.0.0.0:8003/mcp"

# async def scout(topic: str, city: str):
#     async with AsyncExitStack() as stack:
#         # connect to agents and servers
#         contextualist_client = await stack.enter_async_context(Client(CONTEXTUALIST_URL))
#         media_client = await stack.enter_async_context(Client(MEDIA_URL))

#         # 1) Get context data from contextualist agent
#         context_res = await contextualist_client.call_tool(
#             "contextualize",
#             {"topic": topic, "city": city}
#         )

#         # 2) Get media assets from Media Engine
#         media_res = await media_client.call_tool(
#             "search_images",
#             {"query": topic, "per_page": 1}
#         )

#         context = context_res.data
#         media = media_res.data

#     # final report signal
#     final_signal = {
#         "topic": topic,
#         "location": city,
#         "context": context,
#         "media": media
#     }

#     print(json.dumps(final_signal, indent=2, ensure_ascii=False))
#     return final_signal


# if __name__ == "__main__":
#     params = {
#         "topic": "Semiconductor factory opening in Japan",
#         "city": "Tokyo"
#     }
#     asyncio.run(scout(**params))












# import asyncio
# from fastmcp import Client
# import json
# WORLD_DATA_URL = "http://0.0.0.0:8001/mcp"

# async def scout(topic: str):
#     client = Client(WORLD_DATA_URL)

#     async with client:
#         # result is a CallToolResult object
#         result = await client.call_tool(
#             "search_news",
#             {"query": topic}
#         )

#     # ACCESS DATA HERE: Use result.data to get your dictionary
#     news = result.data

#     signal = {
#         "topic": topic,
#         "headline": news.get("headline", "No headline found"),
#         # Note: Your server's search_news tool returns 'source', not 'location'
#         "source": news.get("source", "Unknown source") 
#     }

#     print("Scout Signal:")

#     print(json.dumps(signal, indent=2, ensure_ascii=False))
#     return signal

# if __name__ == "__main__":
#     asyncio.run(scout("Greenland"))
