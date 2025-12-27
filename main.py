# database connection/ retrieval
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())
conn.close()

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_all(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    finally:
        conn.close()
