"""Functions used by the fetch module"""

# Standard library imports
import time
import logging as logger
from typing import Dict, Optional

# Third party imports
import requests
from requests.exceptions import HTTPError, Timeout
from bs4 import BeautifulSoup

# Constants
DEFAULT_DELAY = 3
DEFAULT_RETRIES = 10

def fetch(url: str, retries: Optional[int] = DEFAULT_RETRIES) -> Dict:
    """Download an url handling errors"""
    resp = None
    try:
        logger.info('Downloading: %s', url)
        resp = requests.get(url)
        resp.raise_for_status()
        code = resp.status_code
    except (HTTPError, Timeout):
        logger.exception("Couldn't download: %s", url)
        return None
    if retries > 0 and 500 <= code < 600: # Server error
        logger.info('Retrying download')
        time.sleep(DEFAULT_DELAY)
        return fetch(url, retries-1)
    return resp

#def unzip(url: str, path: str) -> str:
#    pass
#
#def fetch(url: str, character_encoding: Optional[str] = None) -> str:
#    """Download an url"""
#    urllib.request.urlopen(url).read().decode(character_encoding)
#
#async def fetch_async(url: str) -> str:
#    pass
#
#def fetch_json(url: str, character_encoding: str = None) -> Any:
#    pass
#
#async def fetch_json_async(url: str) -> Any:
#    pass
#
#def post(url: str, data: Optional[Dict[str, str]] = None,
#         json_data: Any = None) -> str:
#    pass
#
#def store(url: str, path: str) -> requests.Response:
#    pass
#
#class FetchException(OperationalException):
#    pass
#
#def acceptable_file(filepath: str) -> bool:
#    pass
#
#def escape(str_input: str, skip_double_slash: bool = False) -> str:
#    pass
