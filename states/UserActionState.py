from aiogram.fsm.state import State, StatesGroup


class UserActionState(StatesGroup):
    waiting_for_document = State()  
    menu = State()