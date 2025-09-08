from mcp.server.fastmcp import FastMCP  
import logging
import requests
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Demo")

@mcp.tool(description="Add two integers and return their sum.")
def add(a: int, b: int) -> int:
    """
    Takes two integers and returns their sum.
    Example: add(2, 3) -> 5
    """
    return a + b

@mcp.tool(description="Get current weather for a city")
def weather(city: str) -> str:
    """
    Fetches weather information (condition + temperature) for a given city
    using wttr.in API. Returns a formatted string including city name.
    Example: weather("London") -> "London: Partly cloudy +15°C"
    """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        weather_info = response.text.strip()
        return f"{city.title()}: {weather_info}"
    else:
        return f"Could not fetch weather for {city}. Status code: {response.status_code}"
if __name__ == "__main__":
    logging.info(" Starting MCP server 'Demo'...")
    mcp.run()