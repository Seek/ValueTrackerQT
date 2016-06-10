from hearthstone.objects import *

if __name__ == '__main__':
    import ssl
    import urllib.request
    import json
    import re
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    import pdb

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
                         type=CardType[card.get('type', 'INVALID')].value,
                         rarity=Rarity[card.get('rarity', 'INVALID')].value,
                         cost=card.get('cost', -1), attack=card.get('attack', -1),
                         health=card.get('cost', -1), collectible=card.get('collectible', False),
                         set=CardSet[card.get('set', 'INVALID')].value, flavor=card.get(
                             'flavor', ''),
                         playerClass=CardClass[card.get('playerClass', 'INVALID')].value)
            session.add(card2)

    session.commit()
    pdb.set_trace()
    deck = session.query(Deck).filter_by(id=4)
    deck = Deck(name='Test Deck 2', playerClass=CardClass.WARLOCK.value, date_created=datetime.datetime.now(),
                date_modified=datetime.datetime.now())
    session.add(deck)
    session.commit()
    dcard = session.query(Card).filter_by(id='AT_001').first()
    DeckCard(deck=deck, card=dcard, number=2)
    session.add(Player(name='Test Player', high=0, low=1))
    #m = session.query(Match).filter(Match.id == 1).first()
    # print(m.deck)

    session.commit()
