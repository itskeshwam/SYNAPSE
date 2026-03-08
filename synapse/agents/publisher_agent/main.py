import os
import json
import asyncio
<<<<<<< HEAD
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

=======
from fastmcp import Client, FastMCP
from dotenv import load_dotenv

# Load environment variables such as OPENAI_API_KEY
load_dotenv()

# Initialize the MCP server for the Publisher agent
mcp = FastMCP("Publisher Agent")


@mcp.tool
async def publish_brief(payload: dict) -> dict:
    """
    Generate a daily brief article using an LLM based on aggregated signals.
    """
    # Build the prompt using the aggregated payload
    prompt = f"""
You are a news writer.

Using the news below, write a short daily brief article.
Use a neutral journalistic tone. At the end of the article,
add info about city, its conversion rate and current weather.

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
        model="gpt-5-nano",
        input=prompt,
        max_output_tokens=400
    )

    # Extract the generated article text
    article = response.output_text.strip()

    # Return the article along with the original payload
>>>>>>> 8aa70d185178c1578b65026020f8bc106794e3f2
    return {
        "article": article,
        "payload": payload
    }

<<<<<<< HEAD
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8005)
=======

if __name__ == "__main__":
    # Start the Publisher MCP server
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8005
    )
>>>>>>> 8aa70d185178c1578b65026020f8bc106794e3f2
