"""Functions used by the fetch module"""

# Standard library imports
import urllib.request
from typing import Optional

# Third party imports

# Local application imports

def fetch(url: str, character_encoding: Optional[str] = None) -> str:
    """Download an url"""
    return urllib.request.urlopen(url).read().decode(character_encoding)
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
