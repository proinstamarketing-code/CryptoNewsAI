from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import (
    BOT_TOKEN,
    MODERATION_GROUP_ID,
)

from telegram_bot.keyboards import moderation_keyboard


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


async def send_to_moderation(text: str):

    message = await bot.send_message(
        chat_id=MODERATION_GROUP_ID,
        text=text,
        disable_web_page_preview=True,
        reply_markup=moderation_keyboard(),
    )

    return message