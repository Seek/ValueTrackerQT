import sqlalchemy
from .enums import CardClass, CardSet, CardType, Rarity
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext import mutable
import pdb
import datetime
from bisect import insort

# class JsonEncodedDict(sqlalchemy.TypeDecorator):
#   """Enables JSON storage by encoding and decoding on the fly."""
#   impl = sqlalchemy.String

#   def process_bind_param(self, value, dialect):
#     return json.dumps(value)

#   def process_result_value(self, value, dialect):
#     return json.loads(value)

# mutable.MutableDict.associate_with(JsonEncodedDict)


class Card(Base):
    __tablename__ = "cards"
    id = Column(String, primary_key=True)
    name = Column(String)
    text = Column(String)
    type = Column(Integer)
    rarity = Column(Integer)
    cost = Column(Integer)
    attack = Column(Integer)
    health = Column(Integer)
    collectible = Column(Integer)
    set = Column(Integer)
    flavor = Column(String)
    playerClass = Column(Integer)

    def __repr__(self):
        return "<Card(name='%s', id='%s')>" % (
            self.name, self.id)

    def __lt__(self, other):
        if self.cost == other.cost:
            if self.type == other.type:
                if self.name == other.name:
                    return False
                else:
                    return self.name < other.name
            else:
                return self.type > other.type
        else:
            return self.cost < other.cost


class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    playerClass = Column(Integer)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    cards = association_proxy('deck_cards', 'card')

    def __repr__(self):
        return "<Deck(name='%s', id='%s')>" % (
            self.name, self.id)


class DeckCard(Base):
    __tablename__ = 'deck_cards'
    deck_id = Column(Integer, sqlalchemy.ForeignKey('decks.id'),
                     primary_key=True)
    card_id = Column(Integer, sqlalchemy.ForeignKey('cards.id'),
                     primary_key=True)
    number = Column(Integer)
    deck = relationship(Deck,
                        backref=backref("deck_cards",
                                        cascade="all, delete-orphan"))
    card = relationship(Card)

    def __init__(self, card=None, deck=None, number=None):
        self.card = card
        self.deck = deck
        self.number = number


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    high = Column(Integer)
    low = Column(Integer)

    def __repr__(self):
        return "<Player(name='%s', low='%s')>" % (
            self.name, self.low)


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    opponent_id = Column(Integer, sqlalchemy.ForeignKey('players.id'))
    won = Column(Boolean)
    first = Column(Boolean)
    date = Column(DateTime)
    duration = Column(Integer)
    turns = Column(Integer)
    deck_id = Column(Integer, sqlalchemy.ForeignKey('decks.id'))
    playerClass = Column(Integer)
    opponentClass = Column(Integer)

    deck = relationship("Deck")
    opponent = relationship("Player")

    def __repr__(self):
        return "<Match(id='%s', date='%s')>" % (
            self.name, self.date)
