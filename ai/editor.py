import re


async def edit(text: str):

    if not text:
        return "SKIP"

    # убираем markdown
    text = text.replace("**", "")

    # если модель явно сломалась — сразу пропускаем
    garbage = [
        "We need to produce",
        "Let's think",
        "Here is the article",
        "Certainly!",
        "Sure!",
        "::",
        ")...",
    ]

    for g in garbage:
        if g.lower() in text.lower():
            return "SKIP"

    # если слишком много английского — просим другую модель
    english_words = len(re.findall(r"[A-Za-z]{5,}", text))

    if english_words > 20:
        return "SKIP"

    # единый заголовок
    text = re.sub(
        r"^📰\s*",
        "<b>📰 ",
        text,
        flags=re.MULTILINE,
    )

    if "<b>📰 " in text and "</b>" not in text:
        text = text.replace("\n", "</b>\n", 1)

    # Почему это важно
    text = re.sub(
        r"(💡\s*)?(Why it matters|Почему это важно.*)",
        "<b>💡 Почему это важно?</b>",
        text,
        flags=re.I,
    )

    # Что это значит
    text = re.sub(
        r"(📈\s*)?(What it could mean|What it means|Что это может означать.*|Возможные последствия.*)",
        "<b>📈 Что это значит?</b>",
        text,
        flags=re.I,
    )

    # перевод оставшихся английских заголовков
    text = text.replace("Why it matters", "Почему это важно?")
    text = text.replace("What it could mean", "Что это значит?")
    text = text.replace("What it means", "Что это значит?")

    # убираем лишние пустые строки
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()