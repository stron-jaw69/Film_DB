# tar_streamer.py
import tarfile
import csv
import time
from datetime import datetime
import requests

from config import FASTAPI_BASE_URL, TAR_PATH

PAYMENT_ENDPOINT = f"{FASTAPI_BASE_URL}/payments"
CUSTOMER_ENDPOINT = f"{FASTAPI_BASE_URL}/customers"
CATEGORY_ENDPOINT = f"{FASTAPI_BASE_URL}/categories"

def stream_tar_and_send(tar_path: str, sleep_secs: float = 0.5):
    with tarfile.open(tar_path, "r:*") as tf:
        for member in tf:
            if not member.isfile():
                continue

            # Example assumption: CSV inside with a header containing payment fields
            fileobj = tf.extractfile(member)
            if fileobj is None:
                continue

            # If content is bytes, decode for csv
            lines = (line.decode("utf-8") for line in fileobj)
            reader = csv.DictReader(lines)

            for row in reader:
                # Map row to your actual schema; adjust keys as needed
                payment_payload = {
                    "payment_id": row.get("payment_id"),
                    "payment_ts": datetime.fromisoformat(row["payment_ts"]).isoformat(),
                    "customer_id": row["customer_id"],
                    "category_id": row["category_id"],
                    "amount": float(row["amount"]),
                    "currency": row.get("currency", "USD"),
                    "status": row.get("status", "success"),
                }
                resp = requests.post(PAYMENT_ENDPOINT, json=payment_payload)
                resp.raise_for_status()

                # Optional: also upsert customer/category if present in the same file
                if "customer_first_name" in row:
                    customer_payload = {
                        "customer_id": row["customer_id"],
                        "first_name": row["customer_first_name"],
                        "last_name": row.get("customer_last_name", ""),
                        "email": row.get("customer_email", ""),
                        "country": row.get("customer_country"),
                    }
                    requests.post(CUSTOMER_ENDPOINT, json=customer_payload)

                if "category_name" in row:
                    category_payload = {
                        "category_id": row["category_id"],
                        "name": row["category_name"],
                        "description": row.get("category_description"),
                    }
                    requests.post(CATEGORY_ENDPOINT, json=category_payload)

                # Simulate streaming pace
                time.sleep(sleep_secs)

if __name__ == "__main__":
    stream_tar_and_send(TAR_PATH, sleep_secs=0.5)
