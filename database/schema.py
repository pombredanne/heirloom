"""Create database schema"""
import logging

# Third party imports
from sqlalchemy import engine_from_config, Column, Integer, String, \
        Float, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Local application imports
import config

logging.basicConfig(level=config.LOGGER['level'])
logger = logging.getLogger(__name__)
Base = declarative_base()
engine = engine_from_config(config.DATABASE, prefix='db.')

def layouts():
    return ['normal', 'meld', 'split', 'phenomenon', 'token', 'vanguard', 'double-faced', 'plane', 'flip', 'scheme', 'leveler']

def create_database_schema():
    sql = text('CREATE TABLE version (version TEXT)')
    engine.execute(sql)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([Color(name='White', symbol='W'),
                     Color(name='Blue', symbol='U'),
                     Color(name='Black', symbol='B'),
                     Color(name='Red', symbol='R'),
                     Color(name='Green', symbol='G')])
    session.add_all([Rarity(name='Common'),
                     Rarity(name='Uncommon'),
                     Rarity(name='Rare'),
                     Rarity(name='Mythic Rare'),
                     Rarity(name='Special')])
    session.commit()
    session.close()

class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    layout = Column(String)
    name = Column(String)
    mana_cost = Column(String)
    cmc = Column(String)
    type = Column(String)
    text = Column(String)
    power = Column(String)
    toughness = Column(String)
    loyalty = Column(String)
    image_name = Column(String)
    heirloom_legal = Column(Integer)
    tix = Column(Float)
    usd = Column(Float)
    eur = Column(Float)

class Color(Base):
    __tablename__ = 'color'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)

class CardColor(Base):
    __tablename__ = 'card_color'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    color_id = Column(Integer, ForeignKey('color.id'))

class CardColorIdentity(Base):
    __tablename__ = 'card_color_identity'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    color_id = Column(Integer, ForeignKey('color.id'))

class CardSupertype(Base):
    __tablename__ = 'card_supertype'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    supertype = Column(String, nullable=False)

class CardType(Base):
    __tablename__ = 'card_type'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    type = Column(String, nullable=False)

class CardSubtype(Base):
    __tablename__ = 'card_subtype'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    subtype = Column(String, nullable=False)

class Rarity(Base):
    __tablename__ = 'rarity'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

if __name__ == '__main__':
    create_database_schema()
