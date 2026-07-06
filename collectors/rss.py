import feedparser

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]


def get_news(limit=5):
    news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:limit]:
            news.append({
                "title": entry.title,
                "link": entry.link
            })

    return news