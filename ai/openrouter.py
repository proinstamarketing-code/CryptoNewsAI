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
{article.get("source","")}

Заголовок:
{article.get("title","")}

Полный текст статьи:

{content}
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

                    if status == 200:

                        data = response.json()

                        message = (
                            data.get("choices", [{}])[0]
                            .get("message", {})
                        )

                        content = message.get("content")

                        # Иногда OpenRouter возвращает null
                        if content is None:

                            print("⚠ Пустой content от модели.")

                            await asyncio.sleep(2)

                            continue

                        text = content.strip()

                        if not text:

                            print("⚠ Пустой текст.")

                            await asyncio.sleep(2)

                            continue

                        if text.upper() == "SKIP":

                            return "SKIP"

                        print(f"✅ Использована модель {model}")

                        return text

                    if status == 404:

                        print("Модель недоступна.")

                        break

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

                    if (
                        "429" in str(e)
                        or "No provider available" in str(e)
                    ):

                        if attempt < 3:

                            wait = attempt * 5

                            print(f"Повтор через {wait} сек.")

                            await asyncio.sleep(wait)

                            continue

                    break

            print("➡ Следующая модель...")

            await asyncio.sleep(2)

    print("\n❌ Ни одна модель не ответила.")

    return "SKIP"