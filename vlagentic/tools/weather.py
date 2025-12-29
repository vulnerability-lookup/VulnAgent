from spade_llm import LLMTool


def get_weather(city: str) -> str:
    weather_data = {
        "madrid": "22°C, sunny",
        "london": "15°C, cloudy",
        "new york": "18°C, rainy",
        "tokyo": "25°C, clear",
        "paris": "19°C, partly cloudy",
        "barcelona": "24°C, sunny",
        "luxembourg": "2.3°C, cloudy",
    }
    return weather_data.get(city.lower(), f"No weather data available for {city}")


weather_tool = LLMTool(
    name="get_weather",
    description="Get weather information for a city",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name (e.g., 'Madrid', 'London')",
            }
        },
        "required": ["city"],
    },
    func=get_weather,
)
