import feedparser
from datetime import datetime


RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
}


def get_news(limit=5):

    news = []

    for source, url in RSS_FEEDS.items():

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:limit]:

                news.append(
                    {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", ""),
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