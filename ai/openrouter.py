import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT
from ai.models import get_models


URL = "https://openrouter.ai/api/v1/chat/completions"


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

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=90) as client:

        for model in get_models():

            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": 0.6,
                "max_tokens": 1200,
            }

            try:

                print("=" * 60)
                print("MODEL:", model)

                response = await client.post(
                    URL,
                    headers=headers,
                    json=payload,
                )

                print("STATUS:", response.status_code)

                if response.status_code == 429:

                    print("Лимит модели. Пробуем следующую...")
                    continue

                if response.status_code == 404:

                    print("Модель недоступна. Пробуем следующую...")
                    continue

                response.raise_for_status()

                data = response.json()

                text = (
                    data["choices"][0]["message"]
                    .get("content", "")
                    .strip()
                )

                if not text:

                    print("Пустой ответ.")
                    continue

                if text.upper() == "SKIP":

                    return "SKIP"

                print("Использована модель:", model)

                return text

            except Exception as e:

                print("OPENROUTER ERROR")
                print(model)
                print(e)

                continue

    print("Ни одна модель не ответила.")

    return "SKIP"