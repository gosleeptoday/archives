from aiogram import types
from aiogram.filters.command import CommandStart
from commands import commands_router
from keyboards import start_k
from aiogram.fsm.context import FSMContext
from states import UserActionState


@commands_router.message(CommandStart())
async def command_start_hendler(message: types.Message, state: FSMContext):
    await message.reply("Привет! Используй кнопки для создания архива.", reply_markup=start_k)
    await state.set_state(UserActionState.menu)