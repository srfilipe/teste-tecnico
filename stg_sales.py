from staging_processing import load_and_process_csv, get_existing_hashes, insert_new_records
from app_database import get_connection

def process_sales_data():
    csv_path = "DATA_DIR\\sales_data.csv"
    table_name = "stg.sales_data"
    hash_columns = ['Date','ProductID','ProductName','QuantitySold','Price','Category','CustomerID']

    conn = get_connection()
    sales_df = load_and_process_csv(csv_path, hash_columns)
    existing_hashes = get_existing_hashes(conn, table_name)
    new_records = sales_df[~sales_df['HashID'].isin(existing_hashes)]
    if not new_records.empty:
        insert_new_records(conn, new_records, table_name)
