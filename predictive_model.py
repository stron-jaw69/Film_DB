# models.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from main import fetch_all

def load_film_features():
    """
    Build a feature table per film:
    - length, release_year, rental_duration, rental_rate, replacement_cost
    - total_rentals (label base)
    """
    query = """
        SELECT
            f.film_id,
            f.length,
            f.release_year,
            f.rental_duration,
            f.rental_rate,
            f.replacement_cost,
            COUNT(r.rental_id) AS total_rentals
        FROM film f
        LEFT JOIN inventory i ON f.film_id = i.film_id
        LEFT JOIN rental r ON i.inventory_id = r.inventory_id
        GROUP BY f.film_id,
                 f.length,
                 f.release_year,
                 f.rental_duration,
                 f.rental_rate,
                 f.replacement_cost;
    """
    rows = fetch_all(query)
    return pd.DataFrame(rows)


def build_high_rental_model(threshold_quantile=0.8):
    df = load_film_features()
    if df.empty:
        raise RuntimeError("No film data available to train model.")

    # binary label: highly_rented
    threshold = df["total_rentals"].quantile(threshold_quantile)
    df["highly_rented"] = (df["total_rentals"] >= threshold).astype(int)

    feature_cols = [
        "length",
        "release_year",
        "rental_duration",
        "rental_rate",
        "replacement_cost",
    ]
    X = df[feature_cols].fillna(0)
    y = df["highly_rented"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    print("Train accuracy:", model.score(X_train, y_train))
    print("Test accuracy :", model.score(X_test, y_test))

    return model, feature_cols


def get_film_features_for_prediction(film_id, feature_cols):
    query = """
        SELECT
            f.film_id,
            f.length,
            f.release_year,
            f.rental_duration,
            f.rental_rate,
            f.replacement_cost
        FROM film f
        WHERE f.film_id = %s;
    """
    rows = fetch_all(query, (film_id,))
    if not rows:
        return None, None
    df = pd.DataFrame(rows)
    X = df[feature_cols].fillna(0)
    return df, X


def predict_high_rental_prob(model, feature_cols, film_id):
    film_df, X = get_film_features_for_prediction(film_id, feature_cols)
    if film_df is None:
        return None
    prob_high = model.predict_proba(X)[:, 1][0]
    return {
        "film_id": int(film_df["film_id"].iloc[0]),
        "prob_highly_rented": float(prob_high),
    }

'''
def load_film_features():
    query = """
        SELECT
            f.film_id,
            f.length,
            f.release_year,
            f.rental_rate,
            f.replacement_cost,
            COUNT(r.inventory_id) AS total_rentals  -- Simplified count
        FROM film f
        LEFT JOIN inventory i ON f.film_id = i.film_id
        LEFT JOIN rental r ON r.inventory_id = i.inventory_id
        GROUP BY f.film_id, f.length, f.release_year, f.rental_rate, f.replacement_cost;
    """
    rows = fetch_all(query)
    df = pd.DataFrame(rows, columns=[
        'film_id', 'length', 'release_year', 'rental_rate',
        'replacement_cost', 'total_rentals'
    ])
    return df



def build_high_rental_model(threshold_quantile=0.8):
    df = load_film_features()
    threshold = df["total_rentals"].quantile(threshold_quantile)
    df["highly_rented"] = (df["total_rentals"] >= threshold).astype(int)

    feature_cols = ["length", "release_year", "rental_rate", "replacement_cost"]
    X = df[feature_cols].fillna(0)
    y = df["highly_rented"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    print("Train accuracy:", model.score(X_train, y_train))
    print("Test accuracy :", model.score(X_test, y_test))

    return model, feature_cols

def get_film_features_for_prediction(film_id, feature_cols):
    query = """
        SELECT
            f.film_id,
            f.length,
            f.release_year,
            f.rental_rate,
            f.replacement_cost
        FROM film f
        WHERE f.film_id = %s;
    """
    rows = fetch_all(query, (film_id,))
    if not rows:
        return None, None
    df = pd.DataFrame(rows)
    X = df[feature_cols].fillna(0)
    return df, X

def predict_high_rental_prob(model, feature_cols, film_id):
    film_df, X = get_film_features_for_prediction(film_id, feature_cols)
    if film_df is None:
        return None
    prob_high = model.predict_proba(X)[:, 1][0]
    return {
        "film_id": int(film_df["film_id"].iloc[0]),
        "prob_highly_rented": float(prob_high),
    }

'''