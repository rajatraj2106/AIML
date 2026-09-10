from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv("WEATHER_API_KEY")
base_url = os.getenv("WEATHER_BASE_URL")

import requests

#initialize the MCP server
from mcp.server import MCPServer
mcp = MCPServer("weather")

@mcp.tool()
def weather(city: str) -> str:
    """
    Fetch the current weather from OpenWeatherMap API for a given city.
    how to call: get_weather("Hyderabad")
    """
    try:
        url = base_url
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
        
        response = requests.get(url, params=params)
        data = response.json()
    

        if response.status_code != 200 or "weather" not in data:
            return f"⚠️ Could not fetch weather for '{city}'."

        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        location = data["name"]
        return f"📍 {location}: {desc}, {temp}°C"
    
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"

if __name__ == "__main__":
    # Initialize the MCP server to run with standard input/output transport
    mcp.run(transport="stdio")