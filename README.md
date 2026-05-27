# NexaFlow ETL Pipeline 🚗

## Overview

NexaFlow is an end-to-end Data Engineering project that simulates a real-world ETL workflow for automotive sales analytics.

The pipeline extracts raw CSV datasets (Cars, Customers, Sales), performs data cleaning and transformation using Python and Pandas, and loads the processed data into PostgreSQL.

The processed data is visualized using a Streamlit dashboard to generate business insights and KPI monitoring.

This project demonstrates core Data Engineering concepts:
- ETL pipeline development
- Data transformation and cleaning
- Relational database integration (PostgreSQL)
- Workflow orchestration (Apache Airflow)
- Data visualization (Streamlit)
- Containerization using Docker

## Data Source
This project is built using a publicly available Kaggle dataset:

🔗 Raw Car Sales Dataset
https://www.kaggle.com/datasets/yukeshgk/raw-car-sales-data-set

The dataset simulates a real-world automotive sales system including vehicle inventory, customer data, and sales transactions.

## Tech Stack
- Python (Pandas)
- PostgreSQL
- SQLAlchemy
- Apache Airflow
- Streamlit
- Docker & Docker Compose

## Architecture

CSV Data → Airflow DAG → ETL (Extract / Transform / Load) → PostgreSQL → Streamlit Dashboard

## Features

### ETL Pipeline
- Extract data from CSV files
- Clean and normalize datasets
- Load structured data into PostgreSQL

### Airflow Orchestration
- DAG-based workflow execution
- Task scheduling and monitoring

### Data Processing
- Column normalization
- Date parsing and conversion
- Data cleaning and filtering

### Analytics Dashboard
- KPI metrics (sales, customers, cars)
- Revenue analytics
- Top customers & cars
- Interactive dataset preview

### Containerization
- PostgreSQL container
- Airflow container
- Streamlit application container
- Docker Compose orchestration

---

## Running 
### ETL Pipeline
python scripts/etl.py

### Run Airflow
docker compose up airflow

### Run Streamlit Dashboard
streamlit run scripts/dashboard.py

### Run Full System (Docker)
docker compose up --build

Stop system:
docker compose down