# Task 7: Build Publisher Agent to Generate Articles
import os
import json
import asyncio
from fastmcp import Client, FastMCP
from dotenv import load_dotenv

# Load environment variables such as OPENAI_API_KEY
load_dotenv()

# Initialize the MCP server for the Publisher agent
mcp = FastMCP("Publisher Agent")


@mcp.tool
async def publish_brief(payload: dict) -> dict:
    """
    Generate a daily brief article using an LLM (OpenAI).
    """
    
    # Build the prompt using the aggregated payload
    prompt = f"""
    You are a news writer.

    Using the news below, write a short daily brief article.
    Use a neutral journalistic tone. At the end of the article, 
    add info about city, its conversion rate and current weather

    Data:
    {json.dumps(payload, indent=2)}

    Rules:
    - Do not invent facts.
    - If data is missing, say "Not available."
    - Include:
    - headline
    - 2-3 paragraphs
    - a short "Why it matters" section.
    - A section "About the place of news" section mentioning the weather, conversion rate
    """

    # Initialize the OpenAI client with the API key
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Call the OpenAI Responses API to generate the article
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=400
    )

    # Extract the generated article text
    article = response.output_text.strip()

    # Return the article along with the original payload
    return {
        "article": article,
        "payload": payload
    }


if __name__ == "__main__":
    # Start the Publisher MCP server
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=8005
    )



# import json
# from fastmcp import FastMCP
# from synapse.protocol.post_office import read_messages, clear_messages

# mcp = FastMCP("Publisher Agent")

# def format_markdown(signal: dict) -> str:
#     topic = signal["topic"]
#     city = signal["location"]

#     news = signal["context"]["news_headline"]
#     weather = signal["context"]["location"]["weather"]
#     fx = signal["context"]["financial_context"]
#     image = signal["media"]["images"][0]["src"] if signal["media"]["images"] else None

#     markdown = f"""
# # Daily Brief: {topic}

# ## News
# - **Headline:** {news}

# ## Weather
# - **{city}:** {weather}

# ## FX
# - **Rate:** {fx.get('rate')} ({fx.get('currency_code')} → USD)

# ## Image
# - {image if image else "No image found"}
# """
#     return markdown

# @mcp.tool
# def publish(task_id: str = "task-1") -> dict:
#     messages = read_messages()

#     # Find the message for publisher
#     for msg in messages:
#         if msg["task_id"] == task_id and msg["recipient"] == "publisher":
#             signal = msg["payload"]
#             md = format_markdown(signal)
#             return {"markdown": md, "signal": signal}

#     return {"error": "No message found for publisher"}

# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8005)
