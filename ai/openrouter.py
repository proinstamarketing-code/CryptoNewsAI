import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT


async def rewrite(article):

    prompt = PROMPT.format(
        news=f"""
Заголовок:
{article['title']}

Описание:
{article['summary']}
"""
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:

        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

    except Exception as e:

        print(e)

        return f"""📰 {article['title']}"""