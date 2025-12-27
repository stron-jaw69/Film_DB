# app.py
from predictive_model import build_high_rental_model, predict_high_rental_prob
from movie_recom import filter_films
from find_store import recommend_store

from config import DB_CONFIG
import psycopg2

conn = psycopg2.connect(**DB_CONFIG)
def main():
    print("*** Movie Recommendation System🎥 ***")
    keyword = input("Enter a keyword (title/description): ")
    films = filter_films(keyword)

    if not films:
        print("No films found. Enter a different keyword.")
        return

    print("\nTop matches based on your input:")
    for f in films:
        print(f"{f['film_id']}: {f['title']} (rented {f['rental_count']} times)")

    try:
        film_id = int(input("\nSelect film_id for more details: "))
    except ValueError:
        print("Invalid film_id.")
        return

    # Train ML model
    model, feature_cols = build_high_rental_model()

    prob_info = predict_high_rental_prob(model, feature_cols, film_id)
    if prob_info:
        print(
            f"Predicted probability this film is 'highly rented': "
            f"{prob_info['prob_highly_rented']:.2%}"
        )
    else:
        print("Unable to compute high-rental probability for that film.")

    stores = recommend_store(film_id)
    if not stores:
        print("No store is available for this film.")
    else:
        print("\nRecommended stores for this film:")
        for s in stores:
            print(
                f"Store {s['store_id']} - rentals of this film: "
                f"{s['rentals_at_store']}"
            )

if __name__ == "__main__":
    main()

