import logging
import pandas as pd
from columns_to_hash import hashid

logger = logging.getLogger('etl_logger')

def load_and_process_csv(csv_path: str, hash_columns: list) -> pd.DataFrame:
    staging_dataframe = pd.read_csv(csv_path, dtype=str)
    staging_dataframe['HashID'] = staging_dataframe[hash_columns].astype(str).agg(''.join, axis=1).apply(hashid)
    return staging_dataframe

def get_existing_hashes(conn, table_name: str) -> set:
    cursor = conn.cursor()
    cursor.execute(f"SELECT HashID FROM {table_name}")
    return set(row[0] for row in cursor.fetchall())

def insert_new_records(conn, staging_dataframe: pd.DataFrame, table_name: str):
    cursor = conn.cursor()
    columns = staging_dataframe.columns.tolist()
    placeholders = ', '.join('?' for _ in columns)

    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    data = [tuple(row) for row in staging_dataframe.itertuples(index=False, name=None)]

    try:
        cursor.executemany(insert_sql, data)
        conn.commit()
        logger.info(f"{len(data)} records inserted successfully!")

    except Exception as e:
        conn.rollback()
        logger.info(f"Failure during the upsert. Rollbacking... Error detail: {str(e)}")

    finally:
        conn.close()