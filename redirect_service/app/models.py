from dataclasses import dataclass
from datetime import datetime

@dataclass
class ShortURL:
    short_code: str
    long_url: str
    created_at: datetime
