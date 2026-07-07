import httpx

from config import DEEPSEEK_API_KEY
from ai.prompts import PROMPT


async def rewrite(news):

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": PROMPT.format(news=news),
            }
        ],
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=60) as client:

        response = await client.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
        )

        print("=" * 60)
        print("STATUS:", response.status_code)
        print(response.text)
        print("=" * 60)

        try:
            data = response.json()
        except Exception:
            return f"DeepSeek вернул не JSON:\n{response.text}"

        if "choices" not in data:
            return f"Ошибка DeepSeek:\n{data}"

        return data["choices"][0]["message"]["content"]