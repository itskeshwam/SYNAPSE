# /usercode/synapse/mcp-servers/finance-monitor/server.py

# Task 4: Implement Finance MCP Server
import os
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
load_dotenv()

mcp = FastMCP("Finance Monitor Server")


# Preprovided - A helper function to obtain the target currency code from a location
def get_currency_code(location: str) -> dict:
    """
    Dynamically find the 3-letter currency code for any country using REST Countries API.
    """
    # The API can search by country name or capital city
    url = f"https://restcountries.com/v3.1/name/{location}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # If the search fails, try searching as a capital city
        if response.status_code != 200:
            url = f"https://restcountries.com/v3.1/capital/{location}"
            response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()[0]
            # Currencies are stored in a dict where the key is the code (e.g., {"JPY": {...}})
            currencies = data.get("currencies", {})
            if currencies:
                code = list(currencies.keys())[0]
                return {
                    "location": data.get("name", {}).get("common"),
                    "currency_code": code,
                    "symbol": currencies[code].get("symbol")
                }
        
        return {"error": f"Could not find currency for '{location}'", "fallback": "USD"}

    except Exception as e:
        return {"error": str(e), "fallback": "USD"}


# Task 4: Implement Finance MCP Server
@mcp.tool
def get_fx_rate(location: str) -> dict:
# def get_fx_rate(base: str, quote: str) -> dict:
    """
    Get FX rate between two currencies.
    """
    exchange_api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    currency_info = get_currency_code(location) 
    target = currency_info['currency_code']

    url = f"https://v6.exchangerate-api.com/v6/{exchange_api_key}/pair/{target}/USD"
    
    try:
        response = requests.get(url, timeout=10)
        
        # If the search fails, return an error message
        if response.status_code != 200:
            return {"error": f"Could not find currency for '{location}'", "fallback": "USD"}


        if response.status_code == 200:
            print(response.json())
            data = response.json()
            print(data['conversion_rate'])
            return {
                "currency_code": currency_info['currency_code'],
                "rate": data['conversion_rate'],
                "source": "ExchangeRate API"
            }

    except Exception as e:
        return {"error": str(e), "fallback": "USD"}


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8002
    )
