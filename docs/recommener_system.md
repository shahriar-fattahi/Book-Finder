# Recommender System

Our book recommendation system uses your favorite genres to suggest books. Here's how it works:

1. **Calculate Average Scores**: We first calculate your average score for each genre.
2. **Select Top Genres**: Based on these scores, we identify your top five favorite genres.
3. **Recommend Books**: We then recommend books from these top five genres, prioritizing those from the genre with the highest average score. Books from genres outside of these top five are not considered in the recommendations.

The query use for this system:

- Calculate Average Scores and Select Top Genres:

```sql
SELECT genre, ROUND(AVG(rating), 2) as avg_rate
FROM users_user
INNER JOIN reviews ON (users_user.id = reviews.user_id)
INNER JOIN books ON (reviews.book_id = books.id)
WHERE users_user.id = 1
GROUP BY genre
ORDER BY avg_rate DESC
LIMIT 5;
```

- Recommend Books:
  -- Let's say your top five genres are ranked in this order:
  `['Cooking', 'History', 'Adventure', 'Travel', 'Mystery']`

```sql
SELECT id, title, author, genre
FROM books
WHERE genre IN ('Cooking', 'History', 'Adventure', 'Travel', 'Mystery')
ORDER BY
   CASE genre
        WHEN 'Cooking' THEN 1
        WHEN 'History' THEN 2
        WHEN 'Adventure' THEN 3
        WHEN 'Travel' THEN 4
        WHEN 'Mystery' THEN 5
   END
LIMIT 21
OFFSET 21;
```
