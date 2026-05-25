import pandas as pd
from sqlalchemy import create_engine
import os
import logging

# base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# log
LOG_PATH = os.path.join(BASE_DIR, "logs", "etl.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# connect ke DB
engine = create_engine(
    "postgresql+psycopg2://nexa:nexa123@localhost:5432/nexaflow_db"
)

# extract data
def extract():
    print("EXTRACT START")

    cars = pd.read_csv("../data/Cars.csv")
    customers = pd.read_csv("../data/Customers.csv")
    sales = pd.read_csv("../data/Sales.csv")

    print("EXTRACT DONE")
    return cars, customers, sales


# transform data
def transform(cars, customers, sales):
    print("TRANSFORM START")

    cars.columns = cars.columns.str.strip().str.lower().str.replace(" ", "_")
    customers.columns = customers.columns.str.strip().str.lower().str.replace(" ", "_")
    sales.columns = sales.columns.str.strip().str.lower().str.replace(" ", "_")

    # remove junk columns
    cars = cars.loc[:, ~cars.columns.str.contains("^unnamed")]
    customers = customers.loc[:, ~customers.columns.str.contains("^unnamed")]
    sales = sales.loc[:, ~sales.columns.str.contains("^unnamed")]

    # convert date
    sales["sale_date"] = pd.to_datetime(
        sales["sale_date"],
        errors="coerce",
        dayfirst=True
    )

    print("TRANSFORM DONE")
    return cars, customers, sales


# load data
def load(cars, customers, sales):
    print("LOAD START")

    cars.to_sql("cars", engine, if_exists="replace", index=False)
    customers.to_sql("customers", engine, if_exists="replace", index=False)
    sales.to_sql("sales", engine, if_exists="replace", index=False)

    print("LOAD DONE")


# running ETL
def run():
    print("ETL START")

    cars, customers, sales = extract()
    cars, customers, sales = transform(cars, customers, sales)
    load(cars, customers, sales)

    print("ETL FINISHED")


if __name__ == "__main__":
    run()