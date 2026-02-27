import os
import json
import asyncio
import httpx
from dotenv import load_dotenv
from pebble.services import conversation
from pebble.services.conversation import ConversationLog, get_conversation_log
from pebble.config import get_settings
from pebble.agents.tools import TOOLS, run_tool
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
conversation = ConversationLog()

async def chat_llm(messages: list, use_tools: bool = False) -> str:
    payload = {
          "model": get_settings().model,
          "messages": messages,
    }

    if use_tools:
        payload["tools"] = TOOLS

    async with httpx.AsyncClient() as client:
          response = await client.post(
              "https://openrouter.ai/api/v1/chat/completions",
              headers={
                  "Authorization": f"Bearer {API_KEY}",
                  "Content-Type": "application/json",
              },
              json=payload,
              timeout=60.0,
          )
          return response.json()
    

async def chat(user_message: str) -> str:
    conversation.add_user_message(user_message)

    # agentic loop 
    for i in range(5):
        print(f"  [Thinking... iteration {i+1}]")

        data = await chat_llm(conversation.get_history(), use_tools=True)
        if "error" in data:
            print(f"  [API Error: {data['error']}]")
            return f"API Error: {data['error']}"
        assistant_msg = data["choices"][0]["message"]

        # Check for tool calls
        tool_calls = assistant_msg.get("tool_calls", [])

        if not tool_calls:
            final_message = assistant_msg["content"]
            conversation.add_assistant_message(final_message)
            return final_message
        
        conversation.add_assistant_message(assistant_msg["content"])

        if tool_calls:
            for tool in tool_calls:
                tool_name = tool["function"]["name"]
                tool_args = json.loads(tool["function"]["arguments"])
                result  = run_tool(tool_name, **tool_args)
                print(f"  [Tool result: {result}]")
                conversation.add_agent_message(f"Tool {tool_name} called with args: {tool_args}\nResult: {result}")

        # Add assistant message to conversation
        conversation.add_assistant_message(assistant_msg["content"])

    return "Sorry, I couldn't complete that request."


async def main():
    print("Welcome to Pebble! 🪶")

    while True: 
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! 🪶")
            break
        assistant_message = await chat(user_message)
        print(f"Pebble: {assistant_message}")

if __name__ == "__main__":
    asyncio.run(main())