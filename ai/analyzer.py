import re


IMPORTANT_WORDS = [

    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "sec",
    "etf",
    "fed",
    "fomc",
    "inflation",
    "cpi",
    "interest rate",
    "rate",
    "tariff",
    "trump",
    "treasury",
    "mica",
    "blackrock",
    "fidelity",
    "strategy",
    "microstrategy",
    "ripple",
    "xrp",
    "binance",
    "coinbase",
    "bybit",
    "stablecoin",
    "tokenized",
    "gold",
    "oil",
    "nasdaq",
    "s&p",
    "forex",

]


def analyze(article):

    text = f"""
{article.get("title","")}

{article.get("summary","")}
""".lower()

    score = 3

    found = []

    for word in IMPORTANT_WORDS:

        if word in text:

            found.append(word)

            score += 1

    score = min(score, 10)

    category = "Crypto"

    if any(x in text for x in ["gold", "oil", "forex", "nasdaq", "s&p"]):

        category = "Macro"

    elif any(x in text for x in ["sec", "mica", "law", "court"]):

        category = "Regulation"

    elif any(x in text for x in ["bitcoin", "ethereum", "btc", "eth"]):

        category = "Market"

    audience = [

        "Инвесторы",
        "Трейдеры",

    ]

    tags = []

    for word in found[:5]:

        tag = "#" + re.sub(r"[^a-zA-Z0-9]", "", word.title())

        if tag not in tags:

            tags.append(tag)

    return {

        "publish": score >= 5,

        "score": score,

        "category": category,

        "audience": audience,

        "tags": tags,

    }