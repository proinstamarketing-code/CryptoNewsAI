import httpx

from config import OPENROUTER_API_KEY
from ai.prompts import PROMPT


MODEL = "openai/gpt-oss-120b:free"


async def rewrite(article):

    prompt = PROMPT.format(
        news=f"""
Заголовок:
{article.get("title", "")}

Краткое описание:
{article.get("summary", "")}

Полный текст статьи:

{article.get("content", "")}
"""
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
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
        "temperature": 0.3,
        "max_tokens": 1200,
    }

    try:

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            print("STATUS:", response.status_code)

            response.raise_for_status()

            data = response.json()

            print(data)

            answer = data["choices"][0]["message"]["content"]

            if not answer:
                return None

            # ИИ решил пропустить новость
            if "PUBLISH: NO" in answer:
                print("Новость отклонена редактором ИИ")
                return None

            # Берем только текст после TEXT:
            if "TEXT:" in answer:
                answer = answer.split("TEXT:", 1)[1].strip()

            return answer

    except Exception as e:

        print("OPENROUTER ERROR")
        print(e)

        return None