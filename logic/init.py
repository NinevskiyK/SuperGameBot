from logic.StartPage import StartPage
from logic.SendMsg import SendMessage
from logic.City import City
from logic.Cave import Cave
from bd import Mobs, Locations, Items
import asyncio


async def make_default_things(session):
    async with session() as ss:
        # Mobs
        mob1 = Mobs(HP=2, XP=20, ReqLevel=1, AttackType='Normal', Attack=2, Armour=1, MagicArmour=0)
        mob2 = Mobs(HP=100, XP=50, ReqLevel=2, AttackType='Normal', Attack=5, Armour=5, MagicArmour=1)
        #mob3 = Mobs(HP=2, XP=20, ReqLevel=1, AttackType='Magic', Attack=2, Armour=0, MagicArmour=1)
        #mob4 = Mobs(HP=10, XP=20, ReqLevel=2, AttackType='Magic', Attack=5, Armour=1, MagicArmour=5)
        ss.add_all([mob1, mob2])
        # Items
        item1 = Items(ItemName='Магическая буханка хлеба(+5 к здоровью)', Cost=10, CostToSale=1,
                      ItemType='health_potion', HP=5, Attack=0, MagicAttack=0, Armour=0, MagicArmour=0,ReqLevel=1)
        item2 = Items(ItemName='Магическая водка(+10 к здоровью)', Cost=15, CostToSale=1,
                      ItemType='health_potion', HP=10, Attack=0, MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=2)
        ss.add_all([item1, item2])
        # Locations
        location1 = Locations(XCoord=0, YCoord=0, LocationType='City', LocationName='Бункер Сидоровича')
        location2 = Locations(XCoord=1, YCoord=1, LocationType='Cave', LocationName='Зельеватория X-16')
        ss.add_all([location1, location2])

        await ss.commit()


async def init(bot, replicas, session):
    await make_default_things(session)
    send = SendMessage(bot, replicas)
    StartPage(bot, replicas, send, session)
    City(bot, replicas, send, session)
    Cave(bot, replicas, send, session)
    await bot.polling()