from main import fetch_all
def recommend_store(film_id, limit=3):
    query = """
           SELECT st.store_id,
           COUNT(r.rental_id) AS rentals_at_store
           FROM store st
           JOIN inventory i ON st.store_id = i.store_id
           JOIN rental r ON r.inventory_id = i.inventory_id
           WHERE i.film_id = %s
           GROUP BY st.store_id
           ORDER BY rentals_at_store DESC
           LIMIT %s;
       """
    return fetch_all(query, (film_id, limit))
