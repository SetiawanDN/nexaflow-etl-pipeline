import pandas as pd
from sqlalchemy import create_engine
import os
import logging

# base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# setup log
LOG_PATH = os.path.join(BASE_DIR, "logs", "etl.log")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# db connection
engine = create_engine(
    "postgresql+psycopg2://nexa:nexa123@postgres:5432/nexaflow_db"
)

# extract data
def extract():
    try:
        print("EXTRACT START")

        cars = pd.read_csv("../data/Cars.csv")
        customers = pd.read_csv("../data/Customers.csv")
        sales = pd.read_csv("../data/Sales.csv")

        print("EXTRACT DONE")

        return cars, customers, sales

    except Exception as e:
        logging.error(f"EXTRACT ERROR: {e}")
        raise


# transform data
def transform(cars, customers, sales):
    try:
        print("TRANSFORM START")

        # normalize column names
        cars.columns = (
            cars.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        customers.columns = (
            customers.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        sales.columns = (
            sales.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # remove unnamed columns
        cars = cars.loc[:, ~cars.columns.str.contains("^unnamed")]
        customers = customers.loc[:, ~customers.columns.str.contains("^unnamed")]
        sales = sales.loc[:, ~sales.columns.str.contains("^unnamed")]

        # convert sale_date
        sales["sale_date"] = pd.to_datetime(
            sales["sale_date"],
            errors="coerce",
            dayfirst=True
        )

        print("TRANSFORM DONE")

        return cars, customers, sales

    except Exception as e:
        logging.error(f"TRANSFORM ERROR: {e}")
        raise


# load data
def load(cars, customers, sales):
    try:
        print("LOAD START")

        cars.to_sql(
            "cars",
            engine,
            if_exists="replace",
            index=False
        )

        customers.to_sql(
            "customers",
            engine,
            if_exists="replace",
            index=False
        )

        sales.to_sql(
            "sales",
            engine,
            if_exists="replace",
            index=False
        )

        print("LOAD DONE")

    except Exception as e:
        logging.error(f"LOAD ERROR: {e}")
        raise


# run etl pipeline
def run():
    try:
        print("ETL START")

        cars, customers, sales = extract()

        cars, customers, sales = transform(
            cars,
            customers,
            sales
        )

        load(cars, customers, sales)

        print("ETL FINISHED")

    except Exception as e:
        print("ETL FAILED")
        logging.error(f"ETL FAILED: {e}")


# main
if __name__ == "__main__":
    run()