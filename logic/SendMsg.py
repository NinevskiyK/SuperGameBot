"""
Make sending great again!
"""
from random import choice
from telebot.types import ReplyKeyboardMarkup


class SendMessage:
    def __init__(self, bot, replicas):
        self.bot = bot
        self.replicas = replicas

    async def error(self, message):
        await self.bot.send_message(message.chat.id, choice(self.replicas['Error']['0']))

    async def send_message(self, message, replica, insert=None):
        try:
            if type(replica) == list:
                replica = choice(replica)
            replica = str(replica)
            if insert is not None:
                replica = replica.format(*insert)
            return await self.bot.send_message(message.chat.id, replica)
        except:
            await self.error(message)
            return None

    async def send_markup(self, message, replica, keyboard_replicas, insert=None):
        try:
            if type(replica) == list:
                replica = choice(replica)
            replica = str(replica)
            if insert is not None:
                replica = replica.format(*insert)
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for key in keyboard_replicas:
                keyboard.add(key)
            await self.bot.send_message(message.chat.id, replica, reply_markup=keyboard)
        except:
            await self.error(message)
            return None


