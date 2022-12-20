"""
In cave
"""
from logic.Global import GlobalStates
from sqlalchemy import select, func
from bd import Person, Mobs, Items, BackPackItem
from asyncio import sleep

class Cave:
    def __init__(self, bot, replicas, send, session):
        self.bot = bot
        self.replicas = replicas['Cave']
        self.send_message = send.send_message
        self.send_markup = send.send_markup
        self.session = session

        @bot.message_handler(regexp='В путешествие!')
        async def language_handler(message):
            await self.send_message(message, self.replicas['0'])
            async with self.session() as ss:
                stmt = select(BackPackItem).where(BackPackItem.UserID == message.from_user.id)
                res = await ss.execute(stmt)
                res = res.scalars().all()
                hp = 0
                if res is not None:
                    for r in res:
                        stmt = select(Items).where(Items.ItemID == r.ItemID)
                        await ss.delete(r)
                        res1 = await ss.execute(stmt)
                        hp += res1.scalar().HP
                    print(hp)

                stmt = select(Person).where(Person.UserID == message.from_user.id)
                p = await ss.execute(stmt)
                p = p.scalar()
                print(p)
                hp += p.HP
                attack = p.Attack

                stmt = select(Mobs).where(Mobs.ReqLevel <= p.Level).order_by(func.random())
                res = await ss.execute(stmt)
                res = res.scalars().all()[0]
                hp_mob = res.HP
                attack_mob = res.Attack

                print(locals())
                await sleep(5)
                if hp_mob/attack > hp/attack_mob:
                    await self.bot.set_state(message.from_user.id, GlobalStates.end, message.chat.id)
                    await self.send_markup(message, self.replicas['01'], self.replicas['01?'])
                else:
                    p.XP += res.XP
                    while p.XP >= 100:
                        p.XP -= 100
                        p.Level += 1
                        p.Money += 100
                    await ss.commit()
                    await self.bot.set_state(message.from_user.id, GlobalStates.city, message.chat.id)
                    await self.send_markup(message, self.replicas['00'], self.replicas['00?'])