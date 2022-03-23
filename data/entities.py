from config import CONNECTION_STRING
from email.policy import default
from sqlalchemy import create_engine, Integer, String, \
    Column, ForeignKey, Boolean, ARRAY, BigInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(CONNECTION_STRING)

if not database_exists(engine.url):
    create_database(engine.url)


Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer(), primary_key=True)
    max_users = Column(Integer(), default=250, nullable=False)
    session = Column(Boolean(), nullable=False)


class Barrel(Base):
    __tablename__ = 'barrels'
    id = Column(Integer(), primary_key=True)
    num = Column(Integer(), nullable=False)


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer(), primary_key=True, autoincrement=False)
    card_barrels = Column(ARRAY(Integer))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    chat_id = Column(BigInteger(), nullable=False)
    twitch_name = Column(String(100), nullable=True)
    session = Column(Boolean(), default=False, nullable=False)
    card_id = Column(Integer(), ForeignKey('cards.id'), nullable=True)
    card = relationship("Card", lazy='joined')


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    user = relationship("User", lazy='joined')


Base.metadata.create_all(engine)
