import re

# Самые важные темы рынка
HIGH_IMPORTANCE = [
    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "etf",
    "sec",
    "fed",
    "fomc",
    "interest rate",
    "inflation",
    "cpi",
    "tariff",
    "trump",
    "blackrock",
    "fidelity",
    "microstrategy",
    "strategy",
    "ripple",
    "xrp",
    "binance",
    "coinbase",
    "bybit",
    "kraken",
    "stablecoin",
    "usdt",
    "usdc",
    "mica",
    "tokenized",
    "tokenization",
    "gold",
    "oil",
    "nasdaq",
    "s&p",
    "forex",
]

# Слова, повышающие значимость
IMPORTANT_EVENTS = [
    "approve",
    "approved",
    "launch",
    "launches",
    "ban",
    "lawsuit",
    "court",
    "regulation",
    "license",
    "hack",
    "exploit",
    "liquidation",
    "ipo",
    "acquisition",
    "buy",
    "sell",
    "reserve",
    "treasury",
    "partnership",
]

# Темы, которые чаще всего являются "шумом"
LOW_PRIORITY = [
    "podcast",
    "interview",
    "weekly",
    "today in crypto",
    "what happened",
    "price prediction",
    "opinion",
    "sponsored",
]


def analyze(article):

    text = f"""
{article.get("title", "")}

{article.get("summary", "")}
""".lower()

    score = 0
    found = []

    # Проверяем важные темы
    for word in HIGH_IMPORTANCE:
        if word in text:
            score += 2
            found.append(word)

    # Проверяем важные события
    for word in IMPORTANT_EVENTS:
        if word in text:
            score += 2

    # Понижаем рейтинг "шума"
    for word in LOW_PRIORITY:
        if word in text:
            score -= 3

    score = max(0, min(score, 10))

    # Категория
    category = "Crypto"

    if any(x in text for x in ["fed", "inflation", "cpi", "oil", "gold", "nasdaq", "forex"]):
        category = "Macro"

    elif any(x in text for x in ["sec", "court", "regulation", "license", "mica"]):
        category = "Regulation"

    elif any(x in text for x in ["bitcoin", "btc", "ethereum", "eth"]):
        category = "Market"

    elif any(x in text for x in ["hack", "exploit"]):
        category = "Security"

    audience = []

    if category == "Market":
        audience = ["Трейдеры", "Инвесторы"]

    elif category == "Macro":
        audience = ["Инвесторы"]

    elif category == "Regulation":
        audience = ["Инвесторы", "Бизнес"]

    else:
        audience = ["Криптосообщество"]

    tags = []

    for word in found[:5]:

        tag = "#" + re.sub(r"[^a-zA-Z0-9]", "", word.title())

        if tag not in tags:
            tags.append(tag)

    # Публикуем только действительно важные новости
    publish = score >= 6

    print(
        f"Оценка: {score}/10 | "
        f"Категория: {category} | "
        f"Публиковать: {publish}"
    )

    return {
        "publish": publish,
        "score": score,
        "category": category,
        "audience": audience,
        "tags": tags,
    }