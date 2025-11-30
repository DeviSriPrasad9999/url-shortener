from dataclasses import dataclass
from datetime import datetime

@dataclass
class ShortUrl:
    short_code: str
    long_url: str
    created_at: datetime

