from aiogram.utils.keyboard import InlineKeyboardBuilder


def moderation_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Опубликовать",
        callback_data="publish",
    )

    builder.button(
        text="✏️ Редактировать",
        callback_data="edit",
    )

    builder.button(
        text="❌ Отклонить",
        callback_data="reject",
    )

    builder.adjust(1)

    return builder.as_markup()