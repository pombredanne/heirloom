"""Create database schema"""

# Third party imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

# Local application imports
from database import database_helper
DeclarativeBase = declarative_base()

def create_database_schema():
    engine = database_helper.db_connect()

    sql = text('CREATE TABLE version (version TEXT)')
    result = engine.execute(sql)
    DeclarativeBase.metadata.create_all(engine)
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

class Card(DeclarativeBase):
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

class Color(DeclarativeBase):
    __tablename__ = 'color'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)

class CardColor(DeclarativeBase):
    __tablename__ = 'card_color'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    color_id = Column(Integer, ForeignKey('color.id'))

class CardColorIdentity(DeclarativeBase):
    __tablename__ = 'card_color_identity'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    color_id = Column(Integer, ForeignKey('color.id'))

class CardSupertype(DeclarativeBase):
    __tablename__ = 'card_supertype'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    supertype = Column(String, nullable=False)

class CardType(DeclarativeBase):
    __tablename__ = 'card_type'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    type = Column(String, nullable=False)

class CardSubtype(DeclarativeBase):
    __tablename__ = 'card_subtype'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'))
    subtype = Column(String, nullable=False)

class Rarity(DeclarativeBase):
    __tablename__ = 'rarity'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

if __name__ == '__main__':
    create_database_schema()
