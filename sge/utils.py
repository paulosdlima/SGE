from datetime import date, datetime
from typing import Union


def date_converter(date_value: Union[str, date]) -> date:
    """Converte data do tipo string para datetime."""
    if isinstance(date_value, date):
        return date_value
    return datetime.strptime(date_value, '%Y-%m-%d').date()
