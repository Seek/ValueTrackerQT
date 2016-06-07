import sqlalchemy
import json
from enums import CardClass, CardSet, CardType, Rarity

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean

from sqlalchemy.ext import mutable

class JsonEncodedDict(sqla.TypeDecorator):
  """Enables JSON storage by encoding and decoding on the fly."""
  impl = sqlalchemy.String

  def process_bind_param(self, value, dialect):
    return simplejson.dumps(value)

  def process_result_value(self, value, dialect):
    return simplejson.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    type = Column(Enum(CardType))
    rarity = Column(Enum(Rarity))
    cost = Column(Integer)
    attack = Column(Integer)
    health = Column(Integer)
    collectible = Column(Boolean)
    set = Column(Enum(CardSet))
    flavor = Column(String)
    playerClass = Column(Enum(CardClass))


class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True) 
    name = Column(String)
    playerClass = Column(Enum(CardClass))
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    cards = Column(JsonEncodedDict)

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True) 
    name = Column(String)
    high = Column(Integer)
    low = Column(Integer)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    opponent_id = Column(Integer, ForeignKey('players.id')) 
    won = Column(Boolean)
    first = Column(Boolean)
    date = Column(DateTime)
    duration = Column(Integer)
    turns = Column(Integer)
    deck_id = Column(Integer, ForeignKey('decks.id'))
    playerClass = Column(Enum(CardClass))
    opponentClass = Column(Enum(CardClass))

    deck = relationship("Deck", back_populates="matches")
    opponent = relationship("Player", back_populates="matches")

if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///stats.db', echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)