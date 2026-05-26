import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# page config
st.set_page_config(
    page_title="NexaFlow Dashboard",
    page_icon="🚗",
    layout="wide"
)

# db connection
engine = create_engine(
    "postgresql+psycopg2://nexa:nexa123@postgres:5432/nexaflow_db"
)

# load data
cars = pd.read_sql("SELECT * FROM cars", engine)
sales = pd.read_sql("SELECT * FROM sales", engine)
customers = pd.read_sql("SELECT * FROM customers", engine)

# sidebar config
st.sidebar.title("NexaFlow")

st.sidebar.markdown("""
### Project Stack

- Python
- PostgreSQL
- SQLAlchemy
- Streamlit
- Docker
""")

# header config
st.title("NexaFlow Sales Analytics Dashboard")

st.caption(
    "ETL Pipeline | PostgreSQL | Streamlit | Docker"
)

st.divider()

# kpi section config
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cars",
        len(cars)
    )

with col2:
    st.metric(
        "Total Sales",
        len(sales)
    )

with col3:
    st.metric(
        "Customers",
        len(customers)
    )

with col4:
    st.metric(
        "Brands",
        cars["brand"].nunique()
    )

st.divider()

# bussiness insight config
st.subheader("Business Insights")

left, right = st.columns(2)

# top brand
with left:
    st.markdown("### Top 5 Brands")

    top_brand = (
        cars.groupby("brand")
        .size()
        .reset_index(name="total_cars")
        .sort_values(
            by="total_cars",
            ascending=False
        )
        .head(5)
    )

    st.dataframe(
        top_brand,
        width="stretch"
    )

# brand distribution
with right:
    st.markdown("### Brand Distribution")

    brand_df = (
        cars.groupby("brand")
        .size()
        .reset_index(name="total")
    )

    st.bar_chart(
        brand_df.set_index("brand")
    )

st.divider()

# sales performance
st.subheader("Sales Performance")

sales_df = (
    sales.groupby("car_id")["quantity"]
    .sum()
    .reset_index()
    .sort_values(
        by="quantity",
        ascending=False
    )
    .head(10)
)

colA, colB = st.columns(2)

with colA:
    st.markdown("### Top Selling Cars")

    st.dataframe(
        sales_df,
        width="stretch"
    )

with colB:
    st.markdown("### Sales Chart")

    st.bar_chart(
        sales_df.set_index("car_id")
    )

st.divider()

# raw data
st.subheader("Raw Dataset")

with st.expander("Cars Table"):
    st.dataframe(
        cars,
        width="stretch"
    )

with st.expander("Sales Table"):
    st.dataframe(
        sales,
        width="stretch"
    )

with st.expander("Customers Table"):
    st.dataframe(
        customers,
        width="stretch"
    )

# footer config
st.divider()

st.caption(
    "NexaFlow Data Engineering Project - Version 2"
)