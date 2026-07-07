async def main():

    news = get_news(limit=1)

    if not news:
        print("Новостей нет")
        return

    article = news[0]

    text = f"""📰 {article['title']}

🔗 Источник:
{article['link']}"""

    await bot.send_message(
        CHANNEL_ID,
        text,
        disable_web_page_preview=False,
    )

    print("Пост опубликован")