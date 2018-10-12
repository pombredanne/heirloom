# Standard library imports
import json

# Third party imports
from typing import Any, Dict, List, Optional, Tuple, Union
from pkg_resources import parse_version

# Local application imports
#from database.create_database_schema import Card
from database.card_description import CardDescription
import shared.fetch_internal as internal

def all_cards() -> Dict:
    return json.load(internal.fetch('https://mtgjson.com/json/AllCards.json', 'utf-8'))I
    #return json.load(open('AllCards.json'))

def all_sets() -> Dict[str, Dict[str, Any]]:
    pass

def bugged_cards() -> Optional[List[Dict[str, Any]]]:
    pass

def card_aliases() -> List[List[str]]:
    pass

def card_price(cardname: str) -> Dict[str, Any]:
    pass

#def card_price_string(card: Card, short: bool = False) -> str:
#    pass

def website_url(path: str = '/') -> str:
    pass

def legal_cards(force: bool = False, season: str = None) -> List[str]:
    pass

def mtgjson_version() -> str:
    return parse_version(json.loads(internal.fetch('https://mtgjson.com/json/version.json')))

async def mtgo_status() -> str:
    pass

async def person_data_async(person: Union[str, int]) -> Dict[str, Any]:
    pass

def post_discord_webhook(webhook_id: str, webhook_token: str, message: str, name: str = None) -> bool:
    pass

def resources() -> Dict[str, Dict[str, str]]:
    pass

async def scryfall_cards_async() -> Dict[str, Any]:
    pass

def search_scryfall(query: str) -> Tuple[int, List[str]]:
    def get_frontside(scr_card: Dict) -> str:
        pass

def rulings(cardname: str) -> List[Dict[str, str]]:
    pass

def sitemap() -> List[str]:
    pass

def time(q: str) -> str:
    def whatsinstandard() -> Dict[str, Union[bool, List[Dict[str, str]]]]:
        pass
