import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# config
st.set_page_config(
    page_title="NexaFlow Dashboard",
    page_icon="🚗",
    layout="wide"
)

engine = create_engine(
    "postgresql+psycopg2://nexa:nexa123@localhost:5432/nexaflow_db"
)

# load data
cars = pd.read_sql("SELECT * FROM cars", engine)
sales = pd.read_sql("SELECT * FROM sales", engine)
customers = pd.read_sql("SELECT * FROM customers", engine)

# header
st.title("🚗 NexaFlow Sales Analytics Dashboard")
st.caption("ETL Pipeline | PostgreSQL | Streamlit")

st.divider()

# kpi
col1, col2, col3, col4 = st.columns(4)

col1.metric("🚘 Total Cars", len(cars))
col2.metric("💰 Total Sales", len(sales))
col3.metric("👤 Customers", len(customers))
col4.metric("🏷️ Brands", cars["brand"].nunique())

st.divider()

# top insight
st.subheader("📊 Business Insights")

left, right = st.columns(2)

with left:
    st.markdown("### 🏆 Top 5 Brands")

    top_brand = (
        cars.groupby("brand")
        .size()
        .reset_index(name="total_cars")
        .sort_values("total_cars", ascending=False)
        .head(5)
    )

    st.dataframe(top_brand, use_container_width=True)

with right:
    st.markdown("### 📈 Brand Distribution")

    brand_df = cars.groupby("brand").size().reset_index(name="total")
    st.bar_chart(brand_df.set_index("brand"))

st.divider()

# sales analisis performace
st.subheader("📦 Sales Performance")

sales_df = (
    sales.groupby("car_id")["quantity"]
    .sum()
    .reset_index()
    .sort_values("quantity", ascending=False)
    .head(10)
)

colA, colB = st.columns(2)

with colA:
    st.dataframe(sales_df, use_container_width=True)

with colB:
    st.bar_chart(sales_df.set_index("car_id"))

st.divider()

# data tabel
st.subheader("📁 Raw Data")

with st.expander("Cars Table"):
    st.dataframe(cars, use_container_width=True)

with st.expander("Sales Table"):
    st.dataframe(sales, use_container_width=True)

with st.expander("Customers Table"):
    st.dataframe(customers, use_container_width=True)