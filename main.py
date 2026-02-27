import os
import asyncio
import httpx
from dotenv import load_dotenv
from pebble.services import conversation
from pebble.services.conversation import ConversationLog, get_conversation_log

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
conversation = ConversationLog()

async def chat(user_message: str) -> str:
    conversation.add_user_message(user_message)

    async with httpx.AsyncClient() as client:
          response = await client.post(
              "https://openrouter.ai/api/v1/chat/completions",
              headers={
                  "Authorization": f"Bearer {API_KEY}",
                  "Content-Type": "application/json",
              },
              json={
                  "model": "anthropic/claude-sonnet-4",
                  "messages": conversation.get_history(),
              },
              timeout=60.0,
          )
          response.raise_for_status()
    
    data = response.json()
    assistant_message = data["choices"][0]["message"]["content"]
    conversation.add_assistant_message(assistant_message)
    return assistant_message

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