"""
Start and init
"""
from telebot.asyncio_handler_backends import State, StatesGroup
from bd import Person
from logic.Global import GlobalStates
from sqlalchemy import select


class StartStates(StatesGroup):
    name = State()


class StartPage:
    async def recreate_game(self, id_, message):
        async with self.session() as ss:
            try:
                stmt = select(Person).where(Person.UserID == id_)
                result = await ss.execute(stmt)
                player = result.scalars().one()
                player.Level = 1
                player.HP = 20
                player.CurHP = 20
                player.Money = 10
                player.Attack = 20
                player.MagicAttack = 20
                player.XP = 20
                player.Armour = 20
                player.MagicArmour = 0
                player.LocationID = 1
                await ss.commit()
            except:
                await self.error(message)

    async def create_game(self, id_, name, message):
        async with self.session() as ss:
            try:
                a = Person(UserID=id_, Nickname=name, Level=1, HP=20, CurHP=20, Money=10, Attack=1, MagicAttack=1, XP=0,
                           Armour=0, MagicArmour=0, LocationID=1)
                ss.add(a)
                await ss.commit()
                return True
            except:
                await self.send_message(message, self.replicas['0-'])
                return False

    def __init__(self, bot, replicas, send, session):
        self.bot = bot
        self.replicas = replicas['StartPage']
        self.session = session
        self.send_message = send.send_message
        self.send_markup = send.send_markup
        self.error = send.error

        @bot.message_handler(state=GlobalStates.end)
        async def game_over(message):
            await bot.delete_state(message.from_user.id, message.chat.id)
            await bot.set_state(message.from_user.id, StartStates.name, message.chat.id)
            await self.send_message(message, self.replicas['1'])
            await self.recreate_game(message.from_user.id, message)
            await self.bot.set_state(message.from_user.id, GlobalStates.city, message.chat.id)
            await self.send_markup(message, self.replicas['11'], self.replicas['11?'])

        @bot.message_handler(commands=['start'])
        async def get_name(message):
            await bot.delete_state(message.from_user.id, message.chat.id)
            await bot.set_state(message.from_user.id, StartStates.name, message.chat.id)
            await self.send_message(message, self.replicas['0'])

        @bot.message_handler(state=StartStates.name)
        async def start_game(message):
            await self.send_message(message, self.replicas['00'])
            if not await self.create_game(message.from_user.id, message.text, message):
                await game_over(message)
                return
            await self.send_message(message, self.replicas['000'])
            await self.bot.set_state(message.from_user.id, GlobalStates.city, message.chat.id)
            await self.send_markup(message, self.replicas['0000'], self.replicas['0000?'])
