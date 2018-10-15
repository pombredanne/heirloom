"""Getting the price for usd and tix from mtggoldfish"""
# Standard library imports
import traceback
import logging as logger

# Third party imports
from sqlalchemy import engine_from_config
from sqlalchemy.sql import select
from requests_html import HTMLSession

# Local application imports
from shared.fetch_internal import fetch
from database import database_helper
import config

engine = engine_from_config(config.DATABASE, prefix='db.')
logger.basicConfig(level=logger.INFO)

def make_all_cards_list():
    """Make a list with all card prices"""
    with open('shared/sets.txt') as f:
        set_codes = f.read().splitlines()

    get_prices_snapshot(set_codes)

def get_prices_snapshot(set_codes):
    """Get the prices for all sets"""
    for set_code in set_codes:
        logger.info("Get prices for cards in %s", set_code)
        link = "https://www.mtggoldfish.com/index/" + set_code + "#paper"

        session = HTMLSession()
        web = session.get(link)

        update_prices(web, "online")
        update_prices(web, "paper")

def update_prices(web, marker: str) -> None:
    """Scrape the price and name and insert it in the database"""
    db_connection = engine.connect()

    table_class = '.index-price-table-' + marker
    table = web.html.find(table_class, first=True)
    trs = table.find('tr')
    for tr in trs:
        if not tr.find('.card'):
            continue

        tds = tr.find('td')
        if not tds: # empty list
            continue
        cardname = tds[0].text

        cardname = reformat_mtggoldfish_name(cardname)

        price = float(tds[3].text)

        # TODO: add prices individually for each card in each set and check which set has the lowest price during the legality check
        if marker == 'online':
            currency = 'tix'
        elif marker == 'paper':
            currency = 'usd'
        save_price_database(db_connection, cardname, price, currency)

def save_price_database(db_connection, cardname, price, currency) -> None:
    """Save card price in database"""
    try:
        current_price = database_helper.get_value(db_connection, cardname, currency)

        if current_price is None or price < current_price:
            database_helper.update_column(db_connection, cardname, currency, price)
    except:
        traceback.print_exc()
        logger.error("Couldn't get current price for %s", cardname)

def reformat_mtggoldfish_name(cardname: str) -> str:
    """Format card name properly"""
    #cardname = formatEnglishName(thisCard).replace("&#39;", "'").replace("Lim-Dul","Lim-Dûl").replace("Jotun","Jötun");
    #cardname.replace("&#39;", "'").replace("Lim-Dul","Lim-Dûl").replace("Jotun","Jötun");

    # MTGGoldfish doesn't include the accent, but it should, so I add it.
    if cardname == "Seance":
        cardname = "Séance"
    elif cardname == "Dandan":
        cardname = "Dandân"
    elif cardname == "Khabal Ghoul":
        cardname = "Khabál Ghoul"
    elif cardname == "Junun Efreet":
        cardname = "Junún Efreet"
    elif cardname == "Ghazban Ogre":
        cardname = "Ghazbán Ogre"
    elif cardname == "Ifh-Biff Efreet":
        cardname = "Ifh-Bíff Efreet"
    elif cardname == "Ring of Ma'ruf":
        cardname = "Ring of Ma'rûf"

    return cardname

#def readToList(file_name):
#    sets = None
#    with open(file_name) as f:
#        sets = f.read().splitlines()
#    return sets
#
#def readUrlToList(link):
#
#    with open(web) as f:
#        content = f.readlines()
#    content = [x.strip() for x in content] # remove whitespace characters like `\n` at the end of each line
#
#    return content

#def formatEnglishName(String name):
#    String formatted = "";
#    for (int c = 0; c < name.length(); c += 1){
#        char letter = name.charAt(c);
#
#        # Some cards with multiple promo printings have (second promo) or something in parens, this gets rid of that so we don't get duplicates
#        if(letter == '('){
#            formatted = formatted.trim();
#            break;
#        }
#        else
#            formatted += letter;
#    }
#    return formatted;

if __name__ == "__main__":
    make_all_cards_list()
