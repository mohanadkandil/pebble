import httpx
from typing import List, Dict, Any, Optional
from pebble.config import get_settings

async def chat_completion(messages: List[Dict[str, any]], system: str = "", tools: List[Dict[str, Any]] = None) -> str:
    settings = get_settings()

    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)

    payload = {
        "model": settings.model, 
        "messages": full_messages,

    }
    if tools: 
        payload["tools"] = tools
    
    async with httpx.AsyncClient() as client:
          response = await client.post(
              "https://openrouter.ai/api/v1/chat/completions",
              headers={
                  "Authorization": f"Bearer {settings.openrouter_api_key}",
                  "Content-Type": "application/json",
              },
              json=payload,
              timeout=90.0,
          )
          response.raise_for_status()
          return response.json()
        
