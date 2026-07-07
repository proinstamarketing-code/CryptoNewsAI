import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT
from ai.models import get_model


async def rewrite(article, analysis):

    prompt = PROMPT.format(
        news=f"""
Заголовок:
{article["title"]}

Описание:
{article["summary"]}

========================
АНАЛИЗ
========================

Важность:
{analysis.get("score", 5)}/10

Категория:
{analysis.get("category", "Crypto")}

Аудитория:
{", ".join(analysis.get("audience", []))}

Хештеги:
{", ".join(analysis.get("tags", []))}
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
        "temperature": 0.6,
        "max_tokens": 1200,
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

            print("MODEL:", payload["model"])
            print("STATUS:", response.status_code)

            response.raise_for_status()

            data = response.json()

            message = data["choices"][0]["message"]

            text = message.get("content")

            if not text:
                print("Пустой ответ модели.")
                return "SKIP"

            text = text.strip()

            if text.upper() == "SKIP":
                return "SKIP"

            return text

    except Exception as e:

        print("OPENROUTER ERROR")
        print(e)

        return "SKIP"