"""
In city
"""
from telebot.asyncio_handler_backends import State, StatesGroup
from logic.Global import GlobalStates
from sqlalchemy import select
from bd import Person, Locations, Items, BackPackItem


class CityStates(StatesGroup):
    Buying = State()


class City:
    def __init__(self, bot, replicas, send, session):
        self.bot = bot
        self.replicas = replicas['City']
        self.send_message = send.send_message
        self.send_markup = send.send_markup
        self.session = session

        @bot.message_handler(state=GlobalStates.city)
        async def start(message):
            await bot.delete_state(message.from_user.id, message.chat.id)
            async with self.session() as ss:
                stmt = select(Person).where(Person.UserID == message.from_user.id)
                res = await ss.execute(stmt)
                p = res.scalars().one()
                p.CurHP = Person.HP
                location_id = int(p.LocationID)
                stmt = select(Locations.LocationName).where(Locations.LocationID == location_id)
                res = await ss.execute(stmt)
                location_name = res.scalars().one()
                await bot.delete_state(message.from_user.id, message.chat.id)
                await self.send_markup(message, self.replicas['0'], self.replicas["0?"], [location_name])

        @bot.message_handler(state=CityStates.Buying)
        async def buy(message):
            await bot.delete_state(message.from_user.id, message.chat.id)
            await self.bot.set_state(message.from_user.id, GlobalStates.city, message.chat.id)
            async with self.session() as ss:
                stmt = select(Person).where(Person.UserID == message.from_user.id)
                res = await ss.execute(stmt)
                p = res.scalars().one()
                money = p.Money

                stmt = select(Items).where(Items.ItemName == message.text)
                res = await ss.execute(stmt)
                i = res.scalars().one()
                money_needed = i.Cost
                if money < money_needed:
                    await self.send_message(message, self.replicas['010'])
                    await start(message)
                    return

                p.Money = money - money_needed
                item = BackPackItem(UserID=p.UserID, ItemID=i.ItemID)
                ss.add(item)
                await ss.commit()
            await self.send_message(message, self.replicas['011'])
            await start(message)

        @bot.message_handler(regexp='Торговля!')
        async def language_handler(message):
            async with self.session() as ss:
                stmt = select(Person.Level).where(Person.UserID == message.from_user.id)
                res = await ss.execute(stmt)
                lvl = res.scalars().one()
                stmt = select(Items.ItemName).where(Items.ReqLevel <= lvl)
                res = await ss.execute(stmt)
                items_sc = res.scalars()
                items = [item for item in items_sc]
                await bot.set_state(message.from_user.id, CityStates.Buying, message.chat.id)
                await self.send_markup(message, self.replicas['01'], items)

        @bot.message_handler(regexp='Инфа про себя')
        async def language_handler(message):
            async with self.session() as ss:
                stmt = select(Person).where(Person.UserID == message.from_user.id)
                res = await ss.execute(stmt)
                p = res.scalars().one()
                lvl = p.Level
                money = p.Money
                xp = p.XP
                await self.send_message(message, self.replicas['02'], [lvl, money, xp])
                await start(message)



