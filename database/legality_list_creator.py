# Standard library imports
import logging as logger

# Third party imports
from sqlalchemy import engine_from_config

# Local application imports
from database.database_helper import select_all_cards
import config

logger.basicConfig(level=logger.INFO)
engine = engine_from_config(config.DATABASE, prefix='db.')

def update_legal_cards():
    db_connection = engine.connect()
    cards = select_all_cards(db_connection)
    for card in cards:
        if getattr(card, 'usd') is not None and getattr(card, 'usd') <= 0.5 \
                and getattr(card, 'tix') is not None and getattr(card, 'tix') <= 0.2:
            print(card) # TODO: the card is legal so modify the database accordingly

if __name__ == '__main__':
    update_legal_cards()
