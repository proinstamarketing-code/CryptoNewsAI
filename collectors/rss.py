import re
import html
from datetime import datetime

import feedparser


RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
}


def clean_html(text: str) -> str:

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(r"<[^>]+>", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_news(limit=5):

    news = []

    for source, url in RSS_FEEDS.items():

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:limit]:

                news.append(
                    {
                        "title": clean_html(
                            entry.get("title", "")
                        ),
                        "summary": clean_html(
                            entry.get("summary", "")
                        ),
                        "link": entry.get("link", ""),
                        "source": source,
                        "published": entry.get(
                            "published",
                            datetime.now().isoformat(),
                        ),
                    }
                )

        except Exception as e:

            print(f"Ошибка RSS {source}: {e}")

    unique = {}

    for item in news:
        unique[item["link"]] = item

    news = list(unique.values())

    news.sort(
        key=lambda x: x["published"],
        reverse=True,
    )

    return news