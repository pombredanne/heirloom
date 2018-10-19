from sqlalchemy import engine_from_config, Column, Integer, String, \
        Float, ForeignKey, text

from website.main import Base

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
    tix = Column(Float)
    usd = Column(Float)
    eur = Column(Float)

    def __repr__(self):
        return '<Card %s>' % (self.name)

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
