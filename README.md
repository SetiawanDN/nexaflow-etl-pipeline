# NexaFlow ETL Pipeline 🚗

## Overview

NexaFlow is an end-to-end Data Engineering project that simulates a real-world ETL workflow for automotive sales analytics.

The pipeline extracts raw CSV datasets containing vehicle inventory, customer information, and sales transactions, then performs data cleaning and transformation using Python and Pandas before loading the processed data into PostgreSQL.

The processed data is visualized through an interactive Streamlit dashboard to generate business insights and sales analytics.

This project demonstrates fundamental Data Engineering concepts including:
- ETL pipeline development
- Data transformation and cleaning
- Relational database integration
- Analytics reporting
- Dashboard visualization
- Docker containerization

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
- Docker

## Features

### ETL Pipeline
- Extract raw CSV datasets
- Transform and clean inconsistent data
- Load processed data into PostgreSQL

### Data Processing
- Column normalization
- Date conversion
- Removal of invalid columns
- Structured tabular modeling

### Analytics Dashboard
- KPI monitoring
- Brand distribution analysis
- Sales performance visualization
- Interactive raw dataset preview

### Containerization
- Dockerized PostgreSQL database
- Dockerized Streamlit application
- Multi-container orchestration using Docker Compose

## Run ETL Pipeline
python scripts/etl.py

## Run Streamlit Dashboard
streamlit run scripts/dashboard.py

## Run with Docker
Build and start containers:
docker compose up --build

Run in background mode:
docker compose up -d

Stop containers:
docker compose down

## Dashboard Preview
The Streamlit dashboard includes:

- Business KPI metrics
- Top car brands analysis
- Sales performance visualization
- Interactive data tables

## Future Improvements
- Apache Airflow orchestration
- dbt transformation layer
- Kafka streaming pipeline
- CI/CD integration
- Cloud deployment
- Monitoring and observability