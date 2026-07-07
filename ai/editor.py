from ai.openrouter import rewrite


async def review(article):
    """
    Редактор оценивает новость.

    Пока используем существующую функцию rewrite().
    Позже здесь появится отдельный промпт редактора.
    """

    return await rewrite(article)