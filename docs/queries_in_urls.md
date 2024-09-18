# My ORM and Queries

## List Book

1. all books: `http://127.0.0.1:8000/api/book/list/?limit=2&offset=4&genre=Adventure`
2. specific genre: `http://127.0.0.1:8000/api/book/list/?limit=2&offset=4&genre=Adventure`

The query use for this api:

- all:

  ```sql
  SELECT id, title, author, genre
  FROM books
  LIMIT 21
  OFFSET 21;
  ```

- specific genre:
  -- one query for books:

  ```sql
  SELECT id, title, author, genre
  FROM books
  WHERE genre = 'Adventure'
  LIMIT 21
  OFFSET 21;
  ```

  -- "and a query is used to fetch reviews for books, effectively preventing the N+1 problem."

  ```sql
    SELECT reviews.id, reviews.book_id, users_user.id AS user_id, users_user.username, rating
    FROM reviews
    INNER JOIN users_user ON (reviews.user_id = users_user.id)
    WHERE reviews.book_id IN (1,2,3) AND user_id = 1;
  ```

## Add a review

3. create a review: `http://127.0.0.1:8000/api/book/review/create/`

The query use for this api:

```sql
INSERT INTO reviews (user_id, book_id, rating)
VALUES (1, 2, 5) RETURNING *;
```

## Update a review

3. update a review: `http://127.0.0.1:8000/api/book/review/50/update/`

The query use for this api:

```sql
UPDATE reviews SET rating = 5
WHERE id = 50;
```

## Delete a review

3. delete a review: `http://127.0.0.1:8000/api/book/review/50/delete/`

The query use for this api:

```sql
DELETE FROM reviews
WHERE id = 50;
```
