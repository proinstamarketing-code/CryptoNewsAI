import httpx

from ai.prompts import PROMPT
from ai.models import MODELS

from config import OPENROUTER_API_KEY


API_URL = "https://openrouter.ai/api/v1/chat/completions"


async def ask_model(model: str, prompt: str):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.4,
    }

    async with httpx.AsyncClient(timeout=90) as client:

        response = await client.post(
            API_URL,
            headers=headers,
            json=payload,
        )

        print(f"{model} -> {response.status_code}")

        if response.status_code != 200:
            return None

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return None


async def rewrite(article):

    prompt = PROMPT.format(
        news=f"""
Заголовок:
{article.get("title","")}

Описание:
{article.get("summary","")}

Полный текст:
{article.get("content","")}
"""
    )

    for model in MODELS:

        try:

            print(f"Пробуем модель: {model}")

            result = await ask_model(model, prompt)

            if result:

                print(f"Успешно: {model}")

                if "PUBLISH: NO" in result:
                    return None

                if "TEXT:" in result:
                    return result.split("TEXT:", 1)[1].strip()

                return result.strip()

        except Exception as e:

            print(model)
            print(e)

            continue

    print("Ни одна модель не ответила.")

    return None