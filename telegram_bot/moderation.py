from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "publish")
async def publish(callback: CallbackQuery):

    await callback.answer(
        "🚀 Публикация скоро появится",
        show_alert=True,
    )


@router.callback_query(F.data == "reject")
async def reject(callback: CallbackQuery):

    await callback.message.edit_reply_markup()

    await callback.answer("❌ Новость отклонена")


@router.callback_query(F.data == "edit")
async def edit(callback: CallbackQuery):

    await callback.answer(
        "✏️ Редактирование появится на следующем этапе",
        show_alert=True,
    )