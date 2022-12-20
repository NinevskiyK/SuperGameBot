from telebot.asyncio_handler_backends import State, StatesGroup


class GlobalStates(StatesGroup):
    city = State()
    cave = State()
    end = State()
    city_choose = State()
    cave_choose = State()