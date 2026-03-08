import os
import json
import asyncio
from fastmcp import FastMCP
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

mcp = FastMCP("Publisher Agent")

@mcp.tool
async def publish_brief(payload: dict) -> dict:
    """
    Generate a daily brief article using Groq based on aggregated signals.
    """
    prompt = f"""
    You are a professional news writer.
    Using the news data below, write a short daily brief article in a neutral journalistic tone.
    At the end, add a section about the place's weather and currency rate.

    Data: {json.dumps(payload, indent=2)}

    Rules:
    - Include a Headline.
    - Write 2-3 concise paragraphs.
    - Include a "Why it matters" section.
    """

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Standard Chat Completion call (replacing the invalid responses.create)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    article = response.choices[0].message.content.strip()

    return {
        "article": article,
        "payload": payload
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8005)