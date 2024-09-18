from typing import Dict, Union

from django.db import connection

from config.database import BaseModelManager, dictfetchall


class BookManager(BaseModelManager):
    def create(self, *, title, auther, genre) -> Dict[str, Union[str, int]]:
        query = f"""
                    INSERT INTO {self.table}(title, author, genre)
                    VALUES (%s, %s, %s) RETURNING *;
                """
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, [title, auther, genre])
            except Exception as e:
                raise e
            else:
                return dictfetchall(cursor=cursor)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
