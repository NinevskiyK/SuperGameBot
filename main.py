import configparser
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
import json
from logic.init import init as init_bot
import bd
import asyncio

config = configparser.ConfigParser()
config.read("config.ini")
token = config["BOT"]["token"]

replicas = json.load(open("replicas.json"))

Session = bd.init()

bot = AsyncTeleBot(token)
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
asyncio.run(init_bot(bot, replicas, Session))














