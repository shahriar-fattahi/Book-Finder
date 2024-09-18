from typing import Dict, List, Optional, Union

from django.db import connection
from pydantic import BaseModel

from apps.users.schemas import User as UserSchema
from config.database import BaseModelManager, dictfetchall, dictfetchone


class BookManager(BaseModelManager):
    def create(
        self, *, title: str, auther: str, genre: str
    ) -> Dict[str, Union[str, int]]:
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
                if data is None:
                    return None
                book = Book(**data)
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

    def all(
        self,
        user_id: int,
        limit: int = 21,
        offset: int = 0,
    ) -> List[BaseModel]:
        from .schemas import Book, Review

        with connection.cursor() as cursor:
            try:
                query = f"""
                        SELECT id, title, author, genre FROM {self.table}
                        LIMIT %s OFFSET %s;
                    """
                cursor.execute(query, [limit, offset])
            except Exception as e:
                raise e
            else:
                data = dictfetchall(cursor=cursor)
                if len(data) == 0:
                    return []
                ids = [e["id"] for e in data]

                with connection.cursor() as cursor:
                    query = f"""
                        SELECT reviews.id, reviews.book_id, users_user.id AS user_id, users_user.username, rating 
                        FROM reviews
                        INNER JOIN users_user ON (reviews.user_id = users_user.id)
                        WHERE reviews.book_id IN {*ids,} AND user_id = %s;
                    """
                    cursor.execute(query, [user_id])
                    reviews = dictfetchall(cursor=cursor)

                    books: List[Book] = []
                    for d in data:
                        book = Book(**d)
                        books.append(book)
                        for review in reviews:
                            if book.id == review["book_id"]:
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
                return books

    def filter(
        self, genre, user_id, limit: int = 21, offset: int = 0
    ) -> List[BaseModel]:
        from .schemas import Book, Review

        with connection.cursor() as cursor:
            try:
                query = f"""
                        SELECT id, title, author, genre FROM {self.table} 
                        WHERE genre = %s
                        LIMIT %s OFFSET %s;
                    """
                cursor.execute(
                    query,
                    [genre, limit, offset],
                )
            except Exception as e:
                raise e
            else:
                data = dictfetchall(cursor=cursor)
                if len(data) == 0:
                    return []
                ids = [e["id"] for e in data]

                with connection.cursor() as cursor:
                    query = f"""
                        SELECT reviews.id, reviews.book_id, users_user.id AS user_id, users_user.username, rating 
                        FROM reviews
                        INNER JOIN users_user ON (reviews.user_id = users_user.id)
                        WHERE reviews.book_id IN {*ids,} AND user_id = %s;
                    """
                    cursor.execute(query, [user_id])
                    reviews = dictfetchall(cursor=cursor)

                    books: List[Book] = []
                    for d in data:
                        book = Book(**d)
                        books.append(book)
                        for review in reviews:
                            if book.id == review["book_id"]:
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
                return books

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


class ReviewManager(BaseModelManager):
    def get(
        self,
        review_id: Optional[int] = None,
        book_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[BaseModel]:
        if review_id:
            with connection.cursor() as cursor:
                try:
                    query = f"""
                            SELECT reviews.id, reviews.rating, users_user.id AS user_id, username, books.id as book_id, title, author, genre
                            FROM {self.table}
                            INNER JOIN books ON (reviews.book_id = books.id)
                            INNER JOIN users_user ON (reviews.user_id = users_user.id)
                            WHERE reviews.id = %s;
                        """
                    cursor.execute(
                        query,
                        [review_id],
                    )
                except Exception as e:
                    raise e
                else:
                    data = dictfetchone(cursor=cursor)
        else:
            with connection.cursor() as cursor:
                try:
                    query = f"""
                            SELECT reviews.id, reviews.rating, users_user.id AS user_id, username, books.id as book_id, title, author, genre
                            FROM {self.table}
                            INNER JOIN books ON (reviews.book_id = books.id)
                            INNER JOIN users_user ON (reviews.user_id = users_user.id)
                            WHERE reviews.book_id = %s AND reviews.user_id = %s;
                        """
                    cursor.execute(
                        query,
                        [book_id, user_id],
                    )
                except Exception as e:
                    raise e
                else:
                    data = dictfetchone(cursor=cursor)

        if data is None:
            return None
        from .schemas import Book, Review

        book = Book(
            id=data["book_id"],
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
        )
        user = UserSchema(id=data["user_id"], username=data["username"])

        return Review(id=data["id"], book=book, user=user, rating=data["rating"])

    def create(
        self, user_id: int, book_id: int, rating: int
    ) -> Dict[str, Union[str, int]]:
        query = f"""
                    INSERT INTO {self.table}(user_id, book_id, rating)
                    VALUES (%s, %s, %s) RETURNING *;
                """
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, [user_id, book_id, rating])
            except Exception as e:
                raise e
            else:
                return dictfetchone(cursor=cursor)

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs)

    def update(self, *, review_id: int, rating: int) -> None:
        query = f"""
                    UPDATE {self.table} SET rating = %s
                    WHERE id = %s;
                """
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, [rating, review_id])
            except Exception as e:
                raise e

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
