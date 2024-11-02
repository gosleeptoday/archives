from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

buttons = [
    [types.KeyboardButton(text="printerservis.net")],
    [types.KeyboardButton(text="2 вариант архива")],
    [types.KeyboardButton(text="3 вариант архива")],
    [types.KeyboardButton(text="статистика")]
]

actions_keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

"""
builder_cancel = InlineKeyboardBuilder()
builder_cancel.row(types.InlineKeyboardButton(
    text="Назад", callback_data="cancel")
)
cancel_actions_keyboard = builder_cancel.as_markup()

builder_first= InlineKeyboardBuilder()
builder_first.row(types.InlineKeyboardButton(
    text="Мини сад", callback_data="mini_sad")
)
builder_first.row(types.InlineKeyboardButton(
    text="Детский сад полного дня", callback_data="full_day_sad")
)
builder_first.row(types.InlineKeyboardButton(
    text="Занятия вместе с мамой", callback_data="with_mom")
)
builder_first.row(types.InlineKeyboardButton(
    text="Мероприятия и Дни рождения", callback_data="holidays_birthday")
)

first_actions_keyboard = builder_first.as_markup()

builder_save_cancel= InlineKeyboardBuilder()
builder_save_cancel.row(types.InlineKeyboardButton(
    text="Записаться", callback_data="save")
)
builder_save_cancel.row(types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel")
)
save_cancel_actions_keyboard = builder_save_cancel.as_markup()

builder_with_mom= InlineKeyboardBuilder()
builder_with_mom.row(types.InlineKeyboardButton(
    text="Монтессори вместе с мамой(1-3 года)", callback_data="montessori")
)
builder_with_mom.row(types.InlineKeyboardButton(
    text="Музыкальные занятия Звучалки(6 мес-6 лет)", callback_data="music")
)
builder_with_mom.row(types.InlineKeyboardButton(
    text="Младенческий класс NIDO(6-14 месяцев)", callback_data="nido")
)
builder_with_mom.row(types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel")
)
with_mom_keyboard = builder_with_mom.as_markup()

builder_holiday= InlineKeyboardBuilder()
builder_holiday.row(types.InlineKeyboardButton(
    text="Мероприятия", callback_data="events")
)
builder_holiday.row(types.InlineKeyboardButton(
    text="Дни рождения", callback_data="birthday")
)
builder_holiday.row(types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel")
)
holiday_keyboard = builder_holiday.as_markup()

builder_birth= InlineKeyboardBuilder()
builder_birth.row(types.InlineKeyboardButton(
    text="Каравай-Каравай", callback_data="karavai")
)
builder_birth.row(types.InlineKeyboardButton(
    text="Королевский прием", callback_data="priem")
)
builder_birth.row(types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel")
)
birth_keyboard = builder_birth.as_markup()

builder_confirm = InlineKeyboardBuilder()
builder_confirm.row(types.InlineKeyboardButton(
    text="Подтвердить запись", callback_data="confirm")
)
builder_confirm.row(types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel")
)
confirm_keyboard = builder_confirm.as_markup()"""