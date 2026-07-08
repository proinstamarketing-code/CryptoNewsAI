from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import CHANNEL_ID
from telegram_bot.bot import publish_to_channel

router = Router()


@router.callback_query(F.data == "publish")
async def publish(callback: CallbackQuery):

    text = callback.message.text

    await publish_to_channel(
        CHANNEL_ID,
        text,
    )

    await callback.message.edit_reply_markup()

    await callback.answer(
        "✅ Новость опубликована"
    )


@router.callback_query(F.data == "reject")
async def reject(callback: CallbackQuery):

    await callback.message.edit_reply_markup()

    await callback.answer(
        "❌ Новость отклонена"
    )


@router.callback_query(F.data == "edit")
async def edit(callback: CallbackQuery):

    await callback.answer(
        "✏️ Редактор появится в следующей версии",
        show_alert=True,
    )