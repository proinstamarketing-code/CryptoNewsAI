import asyncio
import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT
from ai.models import get_models

URL = "https://openrouter.ai/api/v1/chat/completions"

RETRY_STATUS = {
    408,
    409,
    425,
    429,
    500,
    502,
    503,
    504,
}


async def rewrite(article, analysis):

    content = article.get("content")

    if not content:
        content = article.get("summary", "")

    prompt = PROMPT.format(
        news=f"""
Источник:
{article.get("source", "")}

Заголовок:
{article["title"]}

Полный текст статьи:

{content}

========================================

АНАЛИЗ

========================================

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

            print("\n" + "=" * 60)
            print(f"🤖 MODEL: {model}")

            for attempt in range(1, 4):

                print(f"Попытка {attempt}/3")

                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    "temperature": 0.55,
                    "max_tokens": 1400,
                }

                try:

                    response = await client.post(
                        URL,
                        headers=headers,
                        json=payload,
                    )

                    status = response.status_code

                    print(f"STATUS: {status}")

                    # --------------------------------------------------
                    # Успех
                    # --------------------------------------------------

                    if status == 200:

                        data = response.json()

                        try:
                            message = data["choices"][0]["message"]
                        except Exception:
                            print("⚠ Некорректный ответ OpenRouter")
                            continue

                        text = message.get("content")

                        if text is None:
                            print("⚠ Пустой content от модели.")
                            await asyncio.sleep(2)
                            continue

                        text = str(text).strip()

                        if not text:
                            print("⚠ Пустой текст.")
                            await asyncio.sleep(2)
                            continue

                        if len(text) > 3500:
                            text = text[:3500]

                        if text.upper() == "SKIP":
                            return "SKIP"

                        print(f"✅ Использована модель {model}")

                        return text

                    # --------------------------------------------------

                    if status == 404:

                        print("Модель недоступна.")

                        break

                    # --------------------------------------------------

                    if status in RETRY_STATUS:

                        print("Временная ошибка.")

                        if attempt < 3:

                            wait = attempt * 5

                            print(f"Повтор через {wait} сек.")

                            await asyncio.sleep(wait)

                            continue

                        print("Лимит попыток для модели.")

                        break

                    print(response.text)

                    break

                except Exception as e:

                    print(e)

                    text = str(e)

                    if (
                        "No provider available" in text
                        or "429" in text
                    ):

                        if attempt < 3:

                            wait = attempt * 5

                            print(f"Повтор через {wait} сек.")

                            await asyncio.sleep(wait)

                            continue

                    break

            print("➡ Переходим к следующей модели...")

            await asyncio.sleep(3)

    print("\n❌ Ни одна модель OpenRouter не ответила.")

    return "SKIP"