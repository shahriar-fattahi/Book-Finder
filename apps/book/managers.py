from typing import Dict, Optional, Union

from django.db import connection
from pydantic import BaseModel

from apps.users.schemas import User as UserSchema
from config.database import BaseModelManager, dictfetchall, dictfetchone


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
                return dictfetchone(cursor=cursor)

    def get(self, book_id: int) -> Optional[BaseModel]:
        from .schemas import Book, Review

        with connection.cursor() as cursor:
            try:
                query = f"""
                        SELECT id, title, author, genre FROM {self.table} WHERE id = %s;
                    """
                cursor.execute(
                    query,
                    [book_id],
                )
            except Exception as e:
                raise e
            else:
                data = dictfetchone(cursor=cursor)
                book = Book(**data)
                if data is None:
                    return None
                with connection.cursor() as cursor:
                    query = f"""
                        SELECT reviews.id, reviews.book_id, users_user.id AS user_id, users_user.username, rating 
                        FROM reviews
                        INNER JOIN users_user ON (reviews.user_id = users_user.id)
                        WHERE reviews.book_id IN ({data['id']});
                    """
                    cursor.execute(query)
                    reviews = dictfetchall(cursor=cursor)
                    for review in reviews:
                        user = UserSchema(
                            id=review["user_id"], username=review["username"]
                        )
                        book.reviews.append(
                            Review(
                                id=review["id"],
                                book=review["book_id"],
                                user=user,
                                rating=review["rating"],
                            )
                        )
                return book

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
