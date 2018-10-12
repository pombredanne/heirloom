from typing import Any, Dict, List

from mypy_extensions import TypedDict

SetCode = str
CardDescription = TypedDict('CardDescription', {
    'layout': str,
    'name': str,
    'manaCost': str,
    'cmc': int,
    'type': str,
    'types': List[str],
    'text': str,
    'names': List[str],
    'imageName': str,
    'rarity': str,
    'printings': List[SetCode],
    'legalities': List[Dict[str, Any]]
})
