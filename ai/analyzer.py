import json
import httpx

from config import OPENROUTER_API_KEY
from ai.models import get_model


ANALYZER_PROMPT = """
Ты — финансовый аналитик.

Твоя задача — решить, стоит ли публиковать новость
в профессиональном Telegram-канале для трейдеров.

Отвечай только JSON.

Формат:

{
  "publish": true,
  "score": 9,
  "category": "ETF",
  "audience": [
    "Инвесторы",
    "Трейдеры"
  ],
  "tags": [
    "Bitcoin",
    "ETF",
    "BlackRock"
  ]
}

Если новость не имеет большого значения,
верни

{
  "publish": false
}

Не добавляй никаких пояснений.

Новость:

{news}
"""


async def analyze(article):

    prompt = ANALYZER_PROMPT.format(
        news=f"""
Заголовок:
{article["title"]}

Описание:
{article["summary"]}
"""
    )

    payload = {
        "model": get_model(),
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            content = data["choices"][0]["message"]["content"]

            return json.loads(content)

    except Exception as e:

        print("ANALYZER ERROR")
        print(e)

        return {
            "publish": True,
            "score": 5,
            "category": "Crypto",
            "audience": [],
            "tags": []
        }