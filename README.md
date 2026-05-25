# NexaFlow ETL Pipeline 🚗

## Overview

NexaFlow is an end-to-end data pipeline project that simulates a real-world data engineering workflow.

The system ingests raw CSV datasets (cars, customers, and sales), performs data cleaning and transformation using Python (Pandas), and loads the processed data into a PostgreSQL database. The results are then visualized through an interactive Streamlit dashboard for business insights.

This project demonstrates core data engineering concepts including ETL design, data modeling, database integration, and basic analytics reporting.

Key focus areas:
- Building a structured ETL pipeline using Python
- Data cleaning and transformation (handling missing and inconsistent data)
- Relational database storage using PostgreSQL
- Data aggregation for business insights
- Interactive dashboard for visualization using Streamlit

## Data Source

This project is built using a publicly available Kaggle dataset:

🔗 Raw Car Sales Dataset  
https://www.kaggle.com/datasets/yukeshgk/raw-car-sales-data-set

The dataset simulates a real-world automotive sales system including vehicle inventory, customer data, and sales transactions.

## Tech Stack
- Python (Pandas)
- PostgreSQL
- SQLAlchemy
- Streamlit

## Features
- ETL pipeline (Extract, Transform, Load)
- Data cleaning & transformation
- Analytics dashboard

## Dashboard Preview
Run locally:
streamlit run scripts/dashboard.py

## ETL Run
python scripts/etl.py