import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

# page config
st.set_page_config(
    page_title="Nexaflow ETL Dashboard",
    layout="wide",
    page_icon="🚀"
)

st.title("🚀 Nexaflow ETL Dashboard (Analytics + Monitoring)")
st.caption("Airflow → PostgreSQL → Streamlit | V4 Hybrid Dashboard")

# db connection
engine = create_engine(
    "postgresql://nexa:nexa123@postgres:5432/nexaflow_db"
)

LOG_FILE = "/opt/airflow/logs/etl.log"

# refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# load data
@st.cache_data(ttl=60)
def load_data():
    cars = pd.read_sql("SELECT * FROM cars", engine)
    customers = pd.read_sql("SELECT * FROM customers", engine)
    sales = pd.read_sql("SELECT * FROM sales", engine)
    return cars, customers, sales

cars, customers, sales = load_data()

sales.columns = sales.columns.str.lower()

# validasi table
def validate_data(cars, customers, sales):
    issues = []
    if cars.empty:
        issues.append("Cars table is empty")
    if customers.empty:
        issues.append("Customers table is empty")
    if sales.empty:
        issues.append("Sales table is empty")
    return issues

issues = validate_data(cars, customers, sales)

for i in issues:
    st.warning(i)

if sales.empty:
    st.error("No sales data found (ETL failed or not run yet)")
    st.stop()

# pipeline health
st.subheader("⚙️ Pipeline Health Check")

try:
    cnt = pd.read_sql("SELECT COUNT(*) as cnt FROM sales", engine)["cnt"][0]

    col1, col2, col3 = st.columns(3)

    if cnt > 0:
        col1.success("Pipeline Healthy")
    else:
        col1.error("Pipeline Broken")

    col2.metric("Total Sales Records", cnt)
    col3.metric("Checked At", datetime.now().strftime("%H:%M:%S"))

except Exception as e:
    st.error(f"DB Error: {e}")

st.divider()

# data freshness
st.subheader("🕒 Data Freshness")

if "sale_date" in sales.columns:
    sales["sale_date"] = pd.to_datetime(sales["sale_date"], errors="coerce")
    last_date = sales["sale_date"].max()

    st.info(f"Latest sales date in DB: {last_date}")
else:
    st.warning("No date column found")

st.divider()

# error log monitoring
st.subheader("🧯 ETL Error Logs")

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()[-30:]

    errors = [l for l in logs if "ERROR" in l]

    if len(errors) > 0:
        st.error("Errors detected in ETL pipeline:")
        for e in errors:
            st.text(e)
    else:
        st.success("No errors in recent logs")
else:
    st.warning("Log file not found")

st.divider()

# kpi section
st.subheader("📊 Business KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cars", len(cars))
col2.metric("Customers", len(customers))
col3.metric("Sales", len(sales))
col4.metric("Unique Customers", sales["customer_id"].nunique())

st.divider()

# revenue
st.subheader("💰 Revenue Analytics")

if {"sale_price", "quantity"}.issubset(sales.columns):

    sales["sale_price"] = sales["sale_price"].fillna(0)
    sales["quantity"] = sales["quantity"].fillna(0)

    sales["revenue"] = sales["sale_price"] * sales["quantity"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${sales['revenue'].sum():,.0f}")
    col2.metric("Avg Revenue", f"${sales['revenue'].mean():,.2f}")
    col3.metric("Max Transaction", f"${sales['revenue'].max():,.0f}")

else:
    st.warning("Missing revenue columns")

st.divider()

# sidebar + filter
st.sidebar.header("Filters")

if "payment_method" in sales.columns:
    method = st.sidebar.multiselect(
        "Payment Method",
        sales["payment_method"].dropna().unique(),
        default=sales["payment_method"].dropna().unique()
    )
    sales = sales[sales["payment_method"].isin(method)]

# top insight
st.subheader("📈 Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("Top Cars")
    st.bar_chart(sales["car_id"].value_counts().head(10))

with col2:
    st.write("Top Customers")
    st.bar_chart(sales["customer_id"].value_counts().head(10))

st.divider()

# payment analysis
st.subheader("💳 Payment Distribution")

st.bar_chart(sales["payment_method"].value_counts())

st.divider()

# sales trend
st.subheader("📅 Sales Trend")

if "sale_date" in sales.columns:
    trend = sales.groupby("sale_date").size()
    st.line_chart(trend)

st.divider()

# data preview
st.subheader("📦 Data Preview")

tab1, tab2, tab3 = st.tabs(["Cars", "Customers", "Sales"])

with tab1:
    st.dataframe(cars.head(20), use_container_width=True)

with tab2:
    st.dataframe(customers.head(20), use_container_width=True)

with tab3:
    st.dataframe(sales.head(20), use_container_width=True)

# footer
st.divider()
st.caption("V3 Dashboard | Analytics + Monitoring Layer | Nexaflow ETL")