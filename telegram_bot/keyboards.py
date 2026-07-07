from aiogram.utils.keyboard import InlineKeyboardBuilder


def moderation_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="✅ Опубликовать",
        callback_data="publish"
    )

    kb.button(
        text="✏️ Редактировать",
        callback_data="edit"
    )

    kb.button(
        text="❌ Отклонить",
        callback_data="delete"
    )

    kb.adjust(1)

    return kb.as_markup()