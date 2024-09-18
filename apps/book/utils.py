from typing import List, Union

from django.db import connection

from config.database import dictfetchall

from .schemas import Book


def recommend_based_on_genre(user_id: int) -> Union[List[Book], str]:
    with connection.cursor() as cursor:
        try:
            query = """
                        SELECT genre, ROUND(AVG(rating), 2) as avg_rate
                        FROM users_user
                        INNER JOIN reviews ON (users_user.id = reviews.user_id)
                        INNER JOIN books ON (reviews.book_id = books.id)
                        WHERE users_user.id = %s
                        GROUP BY genre
                        ORDER BY avg_rate DESC
                        LIMIT 5;
                    """
            cursor.execute(
                query,
                [user_id],
            )
        except Exception as e:
            raise e
        else:
            data = dictfetchall(cursor=cursor)
            if len(data) == 0:
                return "there is not enogh data about you"
            genres = [e["genre"] for e in data]
            try:
                order = "ORDER BY \n   CASE genre \n"
                for index, genre in enumerate(genres):
                    order += f"\t  WHEN '{genre}' THEN {index+1} \n"
                order += "   END"

                query = f"""
                            SELECT id, title, author, genre
                            FROM books
                            WHERE genre IN {*genres,}
                            {order}
                            LIMIT 21;
                        """
                cursor.execute(query, [order])
            except Exception as e:
                raise e
            else:
                data = dictfetchall(cursor=cursor)
                books: List[Book] = []

                for book in data:
                    books.append(Book(**book))

                return books
