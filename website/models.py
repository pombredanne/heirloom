from website.main import db

class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    layout = db.Column(db.String)
    name = db.Column(db.String)
    mana_cost = db.Column(db.String)
    cmc = db.Column(db.String)
    type = db.Column(db.String)
    text = db.Column(db.String)
    power = db.Column(db.String)
    toughness = db.Column(db.String)
    loyalty = db.Column(db.String)
    image_name = db.Column(db.String)
    tix = db.Column(db.Float)
    usd = db.Column(db.Float)
    eur = db.Column(db.Float)

class Color(db.Model):
    __tablename__ = 'color'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    symbol = db.Column(db.String)

class CardColor(db.Model):
    __tablename__ = 'card_color'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))

class CardColorIdentity(db.Model):
    __tablename__ = 'card_color_identity'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))

class CardSupertype(db.Model):
    __tablename__ = 'card_supertype'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    supertype = db.Column(db.String, nullable=False)

class CardType(db.Model):
    __tablename__ = 'card_type'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    type = db.Column(db.String, nullable=False)

class CardSubtype(db.Model):
    __tablename__ = 'card_subtype'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    subtype = db.Column(db.String, nullable=False)

class Rarity(db.Model):
    __tablename__ = 'rarity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
