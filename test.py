from hearthstone.objects import Card, Deck, TrackedDeck
from hearthstone.enums import CardClass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

if __name__ == "__main__":
    sqlengine = create_engine('sqlite:///stats.db', echo=False)
    Session = sessionmaker()
    Session.configure(bind=sqlengine)
    session = Session()

    import pdb

    # deck = session.query(Deck).filter_by(name = 'Test Deck 2').first()

    # track_deck = TrackedDeck(deck)
    # # #Add some cards
    # card = session.query(Card).filter_by(id='AT_002').first()
    # track_deck.add_card(card)

    #pdb.set_trace()
    deck = Deck(name='Test Deck 2',  playerClass=CardClass.SHAMAN.value,
        date_created = datetime.now(), date_modified = datetime.now(), cards=[])

    #Add some cards
    card = session.query(Card).filter_by(id='AT_001').first()

    deck.add_card(card)
    deck.add_card(card)
    deck.add_card(card)
    deck.remove_card(card)
    card = session.query(Card).filter_by(name="Ysera").first()

    deck.add_card(card)
    deck.add_card(card)
    deck.add_card(card)
    deck.remove_card(card)
    
    session.add(deck)
    session.commit()