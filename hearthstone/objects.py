import sqlalchemy
import json
from .enums import CardClass, CardSet, CardType, Rarity

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship

from sqlalchemy.ext import mutable
import pdb
import datetime
from bisect import insort
class JsonEncodedDict(sqlalchemy.TypeDecorator):
  """Enables JSON storage by encoding and decoding on the fly."""
  impl = sqlalchemy.String

  def process_bind_param(self, value, dialect):
    return json.dumps(value)

  def process_result_value(self, value, dialect):
    return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)

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
    cards = Column(JsonEncodedDict)
    def __repr__(self):
        return "<Deck(name='%s', id='%s')>" % (
                    self.name, self.id)

    def add_card(self, card):
        if card in self.cards:
            if self.cards.count(card) >= 2 or card.rarity == Rarity.LEGENDARY:
                return
            else:
                insort(self.cards, card)
        else:
            insort(self.cards, card)

    def remove_card(self, card):
        if card.id in self.cards:
            num_cards = self.cards[card.id]['ndeck']
            if num_cards < 2 or card.rarity == Rarity.LEGENDARY:
                del self.cards[card.id]
            else:
                self.cards[card.id]['ndeck'] -=1

class TrackedDeck:
    def __init__(self, base_deck):
        self.cards = base_deck.cards.copy()

    def add_card(self, card):
        if card.id in self.cards:
            num_cards = self.cards[card.id]['ndeck']
            if num_cards >= 2 or card.rarity == Rarity.LEGENDARY:
                return
            else:
                self.cards[card.id]['ndeck'] +=1
        else:
            self.cards[card.id] = {'ndeck': 1,
                                'nhand' : 0,
                                'nplayed': 0 }

    def remove_card(self, card):
        if card.id in self.cards:
            num_cards = self.cards[card.id]['ndeck']
            if num_cards < 2 or card.rarity == Rarity.LEGENDARY:
                del self.cards[card.id]
            else:
                self.cards[card.id]['ndeck'] -=1

    def card_drawn(self, card):
        if card.id in self.cards:
            self.cards[card.id]['nhand'] += 1
            self.cards[card.id]['ndeck']  -= 1

    def card_played(self, card, where='HAND'):
        if card.id in self.cards:
            if where == 'HAND':
                self.cards[card.id]['nhand'] -= 1
            elif where == 'DECK':
                self.cards[card.id]['ndeck'] -= 1

    def card_shuffled(self, card):
        if card in self.cards:
            self.cards[card.id]['nhand'] -= 1
            self.cards[card.id]['ndeck']  += 1

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

if __name__ == '__main__':
    import ssl
    import urllib.request
    import json
    import re
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///stats.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    def download_cards():
        url = "https://api.hearthstonejson.com/v1/latest/enUS/cards.json"
        def download_hsjson(url):
            context = ssl._create_unverified_context()
            req = urllib.request.urlopen(url, context=context)
            f = req.read()
            with open('cards.json', 'wb') as file:
                file.write(f)
            return f

        raw_data = download_hsjson(url)

        with open('cards.json', 'r', encoding='utf-8') as f:
            cards_json = json.load(f)

        with open('cards.json', 'w', encoding='utf-8') as f:
            json.dump(cards_json, f, sort_keys=True, indent=4)
        
        return cards_json

    # cards_json = download_cards()
    with open('cards.json', 'r', encoding='utf-8') as f:
        cards_json = json.load(f)

    for card in cards_json:
        card2 = session.query(Card).filter_by(id=card['id']).first()
        if card2:
            continue
        else:
            
            card2 = Card(id=card['id'], name=card['name'], text=card.get('text', 'No text'),
                        type = CardType[card.get('type', 'INVALID')].value, 
                        rarity = Rarity[card.get('rarity', 'INVALID')].value,
                        cost = card.get('cost', -1), attack = card.get('attack', -1),
                        health = card.get('cost', -1), collectible = card.get('collectible', False),
                        set = CardSet[card.get('set', 'INVALID')].value, flavor = card.get('flavor', ''), 
                        playerClass = CardClass[card.get('playerClass', 'INVALID')].value)
            session.add(card2)

    # session.add(Deck(name='Test Deck', playerClass = CardClass.WARLOCK.value, date_created = datetime.datetime.now(),
    #             date_modified = datetime.datetime.now(), cards = {}))

    # session.add(Player(name='Test Player', high=0, low=1))
    m = session.query(Match).filter(Match.id == 1).first()
    print(m.deck)

    session.commit()
