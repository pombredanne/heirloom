"""Database functions"""
# Standard library imports
import re

# Third party imports
from typing import Dict
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy_utils.functions import drop_database

# Local application imports
import shared.fetch as fetch
import config_file

def db_connect(): # TODO: type hint Engine
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**config_file.DATABASE))

def update_database(new_version: str):
    """Insert all cards in database"""

    #engine = db_connect()
    engine = create_engine('sqlite:///oracle.sqlite', echo=True)
    drop_database(engine.url)
    cards = fetch.all_cards()
    for name, card in cards.items():
        insert_card(name, card)
    engine.execute('INSERT INTO version (version) VALUES (?)', [new_version])

def insert_card(name: str, card: Dict) -> None:
    """Insert a card in the database"""

    engine = db_connect()
    print(engine.table_names())
    sql = 'INSERT INTO card ('
    sql += ', '.join(property for property in properties())
    sql += ') VALUES ('
    sql += ('?, ' * len(properties())).rstrip(', ')
    sql += ')'
    values = [card.get(underscore2camel(property)) for property in properties()]
    engine.execute(sql, values)
    card_id = engine.value('SELECT last_insert_rowid()')
    for name in card.get('name', []):
        engine.execute('INSERT INTO card_name (card_id, name) VALUES (?, ?)', [card_id, name])
    for color in card.get('colors', []):
        color_id = engine.value('SELECT id FROM color WHERE name = ?', [color])
        engine.execute('INSERT INTO card_color (card_id, color_id) VALUES (?, ?)', [card_id, color_id])
    for symbol in card.get('colorIdentity', []):
        color_id = engine.value('SELECT id FROM color WHERE symbol = ?', [symbol])
        engine.execute('INSERT INTO card_color_identity (card_id, color_id) VALUES (?, ?)', [card_id, color_id])
    for supertype in card.get('supertypes', []):
        engine.execute('INSERT INTO card_supertype (card_id, supertype) VALUES (?, ?)', [card_id, supertype])
    for subtype in card.get('subtypes', []):
        engine.execute('INSERT INTO card_subtype (card_id, subtype) VALUES (?, ?)', [card_id, subtype])

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
