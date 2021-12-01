import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class MealItem:
    name: str
    days_to_serve: int
    last_suggested: Optional[datetime.date]
