from aiogram import Bot

from config import (
    BOT_TOKEN,
    MODERATION_GROUP_ID,
)

from telegram_bot.keyboards import moderation_keyboard


bot = Bot(
    token=BOT_TOKEN,
)


async def send_to_moderation(text: str):

    try:

        message = await bot.send_message(
            chat_id=MODERATION_GROUP_ID,
            text=text,
            disable_web_page_preview=True,
            reply_markup=moderation_keyboard(),
        )

        return message

    except Exception as e:

        print("Ошибка Telegram:")
        print(e)

        return None


async def publish_to_channel(
    channel_id: int,
    text: str,
):

    try:

        await bot.send_message(
            chat_id=channel_id,
            text=text,
            disable_web_page_preview=True,
        )

    except Exception as e:

        print("Ошибка публикации:")
        print(e)