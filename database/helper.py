"""Database functions"""
# Standard library imports
import re
import collections
import logging
from typing import Dict

# Third party imports
from sqlalchemy import engine_from_config, exc
from sqlalchemy_utils.functions import drop_database, database_exists

# Local application imports
from database import schema
from shared import fetch
import config

logging.basicConfig(level=config.LOGGER['level'])
logger = logging.getLogger(__name__)
engine = engine_from_config(config.DATABASE, prefix='db.')

def get_version() -> str:
    db_connection = engine.connect()

    try:
        version = db_connection.execute('SELECT version FROM version').fetchone()
    except: # if version table doesn't exist
        return None
    if version is None:
        return None
    return version[0]


def update_database():
    """Insert all cards in database"""

    new_version = fetch.mtgjson_version()
    current_version = get_version()
    if current_version is not None  and  new_version == current_version:
        return

    # TODO: create the new database in a different file and move to the
    # current file when the prices are updated
    if database_exists(config.DATABASE['db.url']):
        drop_database(engine.url)

    db_connection = engine.connect()
    schema.create_database_schema()
    cards = fetch.all_cards()
    for name, card in cards.items():
        insert_card(name, card)

    from database import price_grabber
    price_grabber.make_all_cards_list()
    update_version(db_connection, new_version)

def update_version(db_connection, version: str):
    try:
        db_connection.execute('INSERT INTO version (version) VALUES (?)', [version])
    except exc.OperationalError:
        logger.error("Attempt to write to read only database")
    db_connection.close()

def insert_card(name: str, card: Dict) -> None:
    """Insert a card in the database"""

    db_connection = engine.connect()
    sql = 'INSERT INTO card ('
    sql += ', '.join(property for property in properties())
    sql += ') VALUES ('
    sql += ('?, ' * len(properties())).rstrip(', ')
    sql += ')'
    values = [card.get(underscore2camel(property)) for property in properties()]
    card_id = db_connection.execute(sql, values).lastrowid
    for color in card.get('colors', []):
        color_id = db_connection.execute('SELECT id FROM color WHERE name = ?', [color]).fetchone()[0]
        db_connection.execute('INSERT INTO card_color (card_id, color_id) VALUES (?, ?)', [card_id, color_id])
    for symbol in card.get('colorIdentity', []):
        color_id = db_connection.execute('SELECT id FROM color WHERE symbol = ?', [symbol]).fetchone()[0]
        db_connection.execute('INSERT INTO card_color_identity (card_id, color_id) VALUES (?, ?)', [card_id, color_id])
    for supertype in card.get('supertypes', []):
        db_connection.execute('INSERT INTO card_supertype (card_id, supertype) VALUES (?, ?)', [card_id, supertype])
    for subtype in card.get('subtypes', []):
        db_connection.execute('INSERT INTO card_subtype (card_id, subtype) VALUES (?, ?)', [card_id, subtype])
    db_connection.close()

def select_all_cards(db_connection):
    sql = 'SELECT ' + ', '.join(property for property in properties2()) \
        + ' FROM card'
    rows = db_connection.execute(sql)
    return [Card2(*row) for row in rows]

def select_null_price_cards():
    db_connection = engine.connect()
    sql = 'SELECT ' + ', '.join(property for property in properties2()) \
        + ' FROM card' \
        + ' WHERE usd is NULL OR tix is NULL'
    rows = db_connection.execute(sql).fetchall()
    print(rows)
    db_connection.close()

def select_legal_cards(expansion):
    db_connection = engine.connect()
    sql = 'SELECT ' + ', '.join(property for property in properties2()) \
        + ' FROM card' \
        + ' WHERE heirloom_legal=1'
    rows = db_connection.execute(sql).fetchall()
    print(rows)
    db_connection.close()

def query(query):
    db_connection = engine.connect()
    sql = 'SELECT ' + ', '.join(property for property in properties2()) \
        + ' FROM card' \
        + ' WHERE name LIKE ?'
    rows = db_connection.execute(sql, ['%' + query + '%'])
    cards = [Card2(*row) for row in rows]
    print(cards)
    db_connection.close()
    return cards

def get_value(db_connection, cardname, column):
    sql = "SELECT {0} FROM card WHERE card.name=?".format(column)
    row = db_connection.execute(sql, (cardname,)).first()
    if not row: # if cardname is not found returns empty list
        return None
    # if column is empty returns tuple with None value
    return row[0]

def update_column(db_connection, cardname, column, price) -> None:
    sql = "UPDATE card SET {0}={1} WHERE name=?".format(column, price)
    row = db_connection.execute(sql, (cardname,))
    # TODO return something to check if ok

def underscore2camel(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

def properties():
    return {
        'layout': 'TEXT',
        'name': 'TEXT',
        'mana_cost': 'TEXT',
        'cmc': 'REAL',
        'type': 'TEXT',
        'text': 'TEXT',
        'power': 'TEXT',
        'toughness': 'TEXT',
        'loyalty': 'TEXT',
        'image_name': 'TEXT'
    }

def properties2():
    return {
        'layout': 'TEXT',
        'name': 'TEXT',
        'mana_cost': 'TEXT',
        'cmc': 'REAL',
        'type': 'TEXT',
        'text': 'TEXT',
        'power': 'TEXT',
        'toughness': 'TEXT',
        'loyalty': 'TEXT',
        'image_name': 'TEXT',
        'heirloom_legal': 'INTEGER',
        'usd': 'FLOAT',
        'tix': 'FLOAT'
    }

Card = collections.namedtuple('Card', properties().keys())
Card2 = collections.namedtuple('Card', properties2().keys())
