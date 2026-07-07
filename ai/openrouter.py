import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT


MODEL = "openrouter/free"


async def rewrite(article):

    prompt = PROMPT.format(
        news=f"""
Заголовок:
{article['title']}

Описание:
{article.get('summary', '')}
"""
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/proinstamarketing-code/CryptoNewsAI",
        "X-Title": "CryptoNewsAI",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.5,
        "max_tokens": 900,
    }

    async with httpx.AsyncClient(timeout=90) as client:

        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        print("STATUS:", response.status_code)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]