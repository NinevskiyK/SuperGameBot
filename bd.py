from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()


class Person(Base):
    __tablename__ = 'players'
    __table_args__ = {'extend_existing': True}

    UserID = Column(Integer, name='UserID', primary_key=True)
    Nickname = Column(String)
    Level = Column(Integer)
    HP = Column(Integer)
    CurHP = Column(Integer)
    Money = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    XP = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    LocationID = Column(Integer, ForeignKey('locations.LocationID'))


class Mobs(Base):
    __tablename__ = 'mobs'

    MobID = Column(Integer, name='MobID', primary_key=True)
    HP = Column(Integer)
    XP = Column(Integer)
    ReqLevel = Column(Integer)
    AttackType = Column(String)
    Attack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = {'extend_existing': True}

    LocationID = Column(Integer, name='LocationID', primary_key=True)
    XCoord = Column(Integer)
    YCoord = Column(Integer)
    LocationType = Column(String)
    LocationName = Column(String)


class Items(Base):
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}

    ItemID = Column(Integer, name='ItemID', primary_key=True)
    ItemName = Column(String)
    Cost = Column(Integer)
    CostToSale = Column(Integer)
    ItemType = Column(String)
    HP = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    ReqLevel = Column(Integer)


class BackPackItem(Base):
    __tablename__ = 'backpack'
    __table_args__ = {'extend_existing': True}

    BackPackItemID = Column(Integer, name='BackPackItemID', primary_key=True)
    UserID = Column(Integer, ForeignKey('players.UserID'))
    ItemID = Column(Integer, ForeignKey('items.ItemID'))


def init():
    engine = create_async_engine('sqlite+aiosqlite:///chinook.db', echo=True, future=True)
    Session = sessionmaker(bind=engine, class_=AsyncSession)
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())
    return Session
