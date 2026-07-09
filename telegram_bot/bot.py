from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from config import (
    BOT_TOKEN,
    MODERATION_GROUP_ID,
)

from telegram_bot.keyboards import moderation_keyboard

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
)


MAX_MESSAGE = 3900


def safe_text(text: str) -> str:
    if len(text) <= MAX_MESSAGE:
        return text

    return text[:MAX_MESSAGE] + "\n\n…"


async def send_to_moderation(text: str):

    text = safe_text(text)

    try:

        message = await bot.send_message(
            chat_id=MODERATION_GROUP_ID,
            text=text,
            disable_web_page_preview=True,
            reply_markup=moderation_keyboard(),
        )

        print("✅ Отправлено в модерацию")

        return message

    except TelegramBadRequest as e:

        print(f"❌ Telegram: {e}")

        return None


async def publish_to_channel(
    channel_id: int,
    text: str,
):

    text = safe_text(text)

    await bot.send_message(
        chat_id=channel_id,
        text=text,
        disable_web_page_preview=True,
    )