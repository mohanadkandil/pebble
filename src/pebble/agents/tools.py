import datetime

TOOLS = [
      {
          "type": "function",
          "function": {
              "name": "get_time",
              "description": "Get current date and time",
              "parameters": {"type": "object", "properties": {}},
          },
      },
      {
          "type": "function",
          "function": {
              "name": "calculate",
              "description": "Calculate math expressions like '2+2' or '100/5'",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "expression": {
                          "type": "string",
                          "description": "Math expression",
                      },
                  },
                  "required": ["expression"],
              },
          },
      },
      {
          "type": "function",
          "function": {
              "name": "get_weather",
              "description": "Get weather for a city",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "city": {
                          "type": "string",
                          "description": "City name",
                      },
                  },
                  "required": ["city"],
              },
          },
      },
]

# Tool implementations
def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression: str):
    try:
          # Only allow safe characters
          allowed = set("0123456789+-*/(). ")
          if not all(c in allowed for c in expression):
              return "Error: Invalid characters"
          return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
      # Fake for now 
      weathers = {
          "tokyo": "72°F, Sunny",
          "london": "58°F, Cloudy",
          "new york": "65°F, Partly Cloudy",
          "cairo": "95°F, Hot and Sunny",
      }
      return weathers.get(city.lower(), f"Weather in {city}: 70°F, Clear")

def run_tool(tool_name: str, **kwargs) -> str:
    if tool_name == "get_time":
        return get_time()
    elif tool_name == "calculate":
        return calculate(kwargs["expression"])
    elif tool_name == "get_weather":
        return get_weather(kwargs["city"])
    else:
        return f"Error: Unknown tool: {tool_name}"