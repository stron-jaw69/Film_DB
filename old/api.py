# api_service.py
from fastapi import FastAPI
from typing import List
from datetime import datetime, timedelta

from config import PaymentIn, CustomerIn, CategoryIn

app = FastAPI(title="Streaming Payments API")

CUSTOMERS = {}
CATEGORIES = {}
PAYMENTS = []  # append-only list

@app.post("/customers", status_code=201)
async def upsert_customer(customer: CustomerIn):
    CUSTOMERS[customer.customer_id] = customer
    return {"ok": True}

@app.post("/categories", status_code=201)
async def upsert_category(category: CategoryIn):
    CATEGORIES[category.category_id] = category
    return {"ok": True}

@app.post("/payments", status_code=201)
async def ingest_payment(payment: PaymentIn):
    PAYMENTS.append(payment)
    return {"ok": True}

@app.get("/metrics/recent")
async def recent_metrics(minutes: int = 5):
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=minutes)
    recent = [p for p in PAYMENTS if p.payment_ts >= cutoff]

    total_amount = sum(p.amount for p in recent)
    total_count = len(recent)

    by_category = {}
    for p in recent:
        by_category.setdefault(p.category_id, 0.0)
        by_category[p.category_id] += p.amount

    return {
        "window_minutes": minutes,
        "total_amount": total_amount,
        "total_count": total_count,
        "by_category": by_category,
    }

@app.get("/customers/{customer_id}")
async def customer_detail(customer_id: str):
    cust = CUSTOMERS.get(customer_id)
    cust_payments = [p for p in PAYMENTS if p.customer_id == customer_id]
    total_amount = sum(p.amount for p in cust_payments)
    return {
        "customer": cust,
        "total_payments": len(cust_payments),
        "total_amount": total_amount,
    }
