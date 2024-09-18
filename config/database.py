from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseModelManager(ABC):
    """
    An interface through which database query operations are provided to Pydantic models.
    At least one Manager exists for every model.
    """

    def __init__(self, db_table_name: str) -> None:
        self.table = db_table_name

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


def dictfetchone(cursor) -> Dict[str, Any]:
    """
    Return first rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))


def dictfetchall(cursor) -> List[Dict[str, Any]]:
    """
    Return all rows from a cursor as a list of dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
