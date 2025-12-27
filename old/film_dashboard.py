# dashboard.py
import streamlit as st
import requests
from config import FASTAPI_BASE_URL

METRICS_ENDPOINT = f"{FASTAPI_BASE_URL}/metrics/recent"
CUSTOMER_ENDPOINT = f"{FASTAPI_BASE_URL}/customers"

st.set_page_config(page_title="Streaming Payments Dashboard", layout="wide")

st.title("Streaming Payments Dashboard")

col1, col2 = st.columns(2)
with col1:
    window = st.slider("Window (minutes)", min_value=1, max_value=60, value=5, step=1)
with col2:
    if st.button("Refresh metrics"):
        st.experimental_rerun()

# Fetch metrics
params = {"minutes": window}
metrics_resp = requests.get(METRICS_ENDPOINT, params=params)
metrics_data = metrics_resp.json()

st.subheader("Global metrics")
c1, c2 = st.columns(2)
c1.metric(label="Total transactions", value=metrics_data["total_count"])
c2.metric(label="Total amount", value=round(metrics_data["total_amount"], 2))

st.subheader("Amount by category")
by_cat = metrics_data["by_category"]
if by_cat:
    cat_rows = [{"category_id": k, "amount": v} for k, v in by_cat.items()]
    st.table(cat_rows)
else:
    st.write("No data in the selected window yet.")

st.subheader("Customer explorer")
customer_id = st.text_input("Customer ID")
if customer_id:
    resp = requests.get(f"{CUSTOMER_ENDPOINT}/{customer_id}")
    if resp.status_code == 200:
        data = resp.json()
        st.write("Customer profile:", data["customer"])
        st.write("Total payments:", data["total_payments"])
        st.write("Total amount:", data["total_amount"])
    else:
        st.warning("Customer not found or no data.")
