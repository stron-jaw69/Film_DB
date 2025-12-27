# recommendation.py
from main import fetch_all

def filter_films(keyword, limit=10):
    query = """
    SELECT f.film_id,
               f.title,
               f.description,
               COUNT(r.rental_id) AS rental_count
    FROM film f
    LEFT JOIN inventory i ON f.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    WHERE f.title ILIKE %s OR f.description ILIKE %s
    GROUP BY f.film_id, f.title, f.description
    ORDER BY rental_count DESC, f.title
    LIMIT %s;
    """
    pattern = f"%{keyword}%"
    return fetch_all(query, (pattern, pattern, limit))
