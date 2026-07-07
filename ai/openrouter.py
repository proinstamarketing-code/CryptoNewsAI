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
        "temperature": 0.4,
        "max_tokens": 700,
    }

    async with httpx.AsyncClient(timeout=90) as client:

        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        message = data["choices"][0]["message"]

        text = message.get("content")

        if text:
            return text.strip()

        return f"""📰 {article['title']}"""