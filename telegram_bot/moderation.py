from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import bot
from config import CHANNEL_ID

router = Router()


@router.callback_query(F.data == "publish")
async def publish(callback: CallbackQuery):

    text = callback.message.text

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        disable_web_page_preview=True,
    )

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer("✅ Новость опубликована")


@router.callback_query(F.data == "reject")
async def reject(callback: CallbackQuery):

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer("❌ Новость отклонена")


@router.callback_query(F.data == "edit")
async def edit(callback: CallbackQuery):

    await callback.answer(
        "✏️ Редактирование появится на следующем этапе",
        show_alert=True,
    )