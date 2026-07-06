import httpx

from config import DEEPSEEK_API_KEY
from ai.prompts import PROMPT


async def rewrite(news):

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": PROMPT.format(news=news)
            }
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:

        response = await client.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]