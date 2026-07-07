from newspaper import Article


def get_article_text(url: str) -> str:
    """
    Скачивает статью и возвращает основной текст.
    Если не удалось — возвращает пустую строку.
    """

    try:

        article = Article(url)

        article.download()

        article.parse()

        text = article.text.strip()

        return text

    except Exception as e:

        print("ARTICLE ERROR:", e)

        return ""