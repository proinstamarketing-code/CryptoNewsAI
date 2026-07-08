import re


async def edit(text: str):

    """
    Финальная редактура текста.

    Пока работает без ИИ.

    Исправляет оформление
    перед публикацией.
    """

    text = text.strip()

    # убираем лишние пустые строки
    text = re.sub(r"\n{3,}", "\n\n", text)

    # пробелы
    text = re.sub(r"[ \t]+", " ", text)

    # пробелы перед переносом
    text = re.sub(r" +\n", "\n", text)

    return text