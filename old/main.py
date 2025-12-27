# config.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

FASTAPI_BASE_URL = "http://localhost:8000"
TAR_PATH = "data/archive.tar"  # path to your .tar file

class PaymentIn(BaseModel):
    payment_id: str
    payment_ts: datetime
    customer_id: str
    category_id: str
    amount: float
    currency: str
    status: str

class CustomerIn(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    country: Optional[str] = None

class CategoryIn(BaseModel):
    category_id: str
    name: str
    description: Optional[str] = None
