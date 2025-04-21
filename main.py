import logging
import sys
import os
from stg_customers import process_customers_data
from stg_sales import process_sales_data
from dw_customers import upsert_customers
from dw_sales import upsert_sales

logger = logging.getLogger("etl_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler('logs\\etl_logs.csv', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def main():
    try:
        logger.info("Initializing the ETL...\n")

        process_customers_data()
        logger.info("Customers pipeline (Staging) finished!")

        process_sales_data()
        logger.info("Sales pipeline (Staging) finished!\n")

        upsert_customers(stg_table="stg.customers_data",dw_table="dw.DimCustomers")
        logger.info("DimCustomers pipeline (Data Warehouse) finished!\n")

        upsert_sales(stg_table="stg.sales_data",dw_table="dw.FactSales")
        logger.info("FactSales pipeline (Data Warehouse) finished!\n")

        logger.info("ETL finished successfully!\n")

    except Exception as e:
        logger.exception(f"ETL pipeline failed: {e} \n")
        sys.exit(1)

if __name__ == "__main__":
    main()
