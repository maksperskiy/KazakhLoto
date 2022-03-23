from config import CONNECTION_STRING
from data.entities import *

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import random


engine = create_engine(CONNECTION_STRING)

session = Session(bind=engine)


def addUser(chat_id):
    session.add(User(
        chat_id=chat_id,
        session=False
    ))
    session.commit()


def userExists(chat_id):
    return session.query(User).filter(User.chat_id == chat_id).count() > 0


def getTwitchName(chat_id):
    return session.query(User).filter(User.chat_id == chat_id).first().twitch_name


def addTwitchName(chat_id, twitch_name):
    user = session.query(User).filter(User.chat_id == chat_id).first()
    user.twitch_name = twitch_name
    session.add(user)
    session.commit()


def isAdmin(chat_id):
    return session.query(User).select_from(Admin).join(Admin.user).filter(User.chat_id == chat_id).count() > 0


def addAdmin(chat_id):
    user_id = session.scalars(session.query(User.id).filter(User.chat_id == chat_id)).first()
    session.add(Admin(
        user_id = user_id
    ))
    session.commit()


def getUserMailing():
    return session.scalars(session.query(User.chat_id)).all()


def getUserMailingInSession():
    return session.scalars(session.query(User.chat_id).filter(User.session)).all()


def getAdmins():
    return session.scalars(session.query(User.chat_id).select_from(Admin).join(Admin.user)).all()


def startSession():
    game = session.query(Game).first()
    game.session = True
    session.add(game)
    session.commit()


def stopSession():
    game = session.query(Game).first()
    game.session = False
    session.add(game)
    session.query(User).update(
        {"session": False, "card_id": None}, synchronize_session='fetch')
    session.query(Barrel).delete(synchronize_session='fetch')
    session.commit()


def isGameStarted():
    return session.scalars(session.query(Game.session)).first()


def connectUser(chat_id):
    user = session.query(User).filter(User.chat_id == chat_id).first()
    user.session = True
    session.add(user)
    session.commit()


def getMaxUsersValue():
    return session.scalars(session.query(Game.max_users)).first()


def addGame():
    if session.query(Game.max_users).count() > 0:
        return
    session.add(Game(
        session=False
    ))
    session.commit()


def addCardToUser(chat_id):
    user = session.query(User).filter(User.chat_id == chat_id).first()
    if user.card_id:
        return user.card_id

    cards = session.scalars(session.query(User.card_id)).all()
    max_count = session.scalars(session.query(Game.max_users)).first()

    card = 0
    while card == 0 or card in cards:
        card = random.randint(1, max_count)

    user.card_id = card
    session.add(user)
    session.commit()
    return card


def getUserCard(chat_id):
    return session.scalars(session.query(User.card_id).filter(User.chat_id == chat_id)).first()


def usersCount():
    return session.query(User).filter(User.session).count()


def getCardBarrels(id):
    return session.scalars(session.query(Card.card_barrels).filter(Card.id == id)).first()


def addNum(barrel):
    session.add(Barrel(
        num=barrel,
    ))
    session.commit()


def getBarrels():
    return session.scalars(session.query(Barrel.num)).all()


def isWin(chat_id):
    card = session.scalars(session.query(Card.card_barrels).select_from(User).join(User.card).\
                filter(User.chat_id == chat_id)).first()
    barrels = getBarrels()
    for el in card:
        if el not in barrels:
            return False
    return True


def addCard(id, barrels):
    session.add(Card(
        id = id,
        card_barrels = barrels
    ))
    session.commit()