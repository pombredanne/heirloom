"""Database functions"""
# Standard library imports
import re
import logging as logger
logger.basicConfig(level=logger.INFO)

# Third party imports
from typing import Dict
from sqlalchemy import exc, create_engine, text, engine_from_config
from sqlalchemy.engine.url import URL
from sqlalchemy_utils.functions import drop_database, database_exists

# Local application imports
from database import create_database_schema
import shared.fetch as fetch
import config

engine = engine_from_config(config.DATABASE, prefix='db.')

def update_database(new_version: str):
    """Insert all cards in database"""

    db_connection = engine.connect()

    if database_exists(config.DATABASE['db.url']):
        drop_database(engine.url)

    create_database_schema.create_database_schema()
    cards = fetch.all_cards()
    for name, card in cards.items():
        insert_card(name, card)
    try:
        db_connection.execute('INSERT INTO version (version) VALUES (?)', [new_version])
    except exc.OperationalError as e:
        logger.error("Attempt to write to read only database")
    db_connection.close()

def insert_card(name: str, card: Dict) -> None:
    """Insert a card in the database"""

    db_connection = engine.connect()
    print(engine.table_names())
    sql = 'INSERT INTO card ('
    sql += ', '.join(property for property in properties())
    sql += ') VALUES ('
    sql += ('?, ' * len(properties())).rstrip(', ')
    sql += ')'
    values = [card.get(underscore2camel(property)) for property in properties()]
    card_id = db_connection.execute(sql, values).lastrowid
    #card_id = db_connection.execute('SELECT last_insert_rowid()').fetchone()
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
      'image_name': 'TEXT',
}
