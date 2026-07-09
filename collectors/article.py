from newspaper import Article
from bs4 import BeautifulSoup
import httpx


async def load_article(url: str, summary: str = "") -> str:
    """
    Загружает полный текст статьи.

    Если Newspaper не смог —
    используем BeautifulSoup.

    Если и он не смог —
    возвращаем RSS summary.
    """

    # ------------------------
    # Newspaper4k
    # ------------------------

    try:

        article = Article(url)

        article.download()

        article.parse()

        text = article.text.strip()

        if len(text) > 500:

            print("✅ Article loaded (newspaper)")

            return text

    except Exception as e:

        print("Newspaper:", e)

    # ------------------------
    # BeautifulSoup
    # ------------------------

    try:

        async with httpx.AsyncClient(
            timeout=20,
            follow_redirects=True,
        ) as client:

            response = await client.get(url)

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        paragraphs = soup.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        if len(text) > 500:

            print("✅ Article loaded (BeautifulSoup)")

            return text

    except Exception as e:

        print("BeautifulSoup:", e)

    print("⚠ Используем RSS summary.")

    return summary