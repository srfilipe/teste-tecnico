import logging
from datetime import datetime
from app_database import get_connection

logger = logging.getLogger('etl_logger')

def upsert_customers(stg_table: str, dw_table: str):
    conn = get_connection()
    cursor = conn.cursor()
    load_date = datetime.now()

    update_sql = f"""
        UPDATE target
        SET
            EndDate = ?,
            IsCurrent = 0
        FROM {dw_table} AS target
        JOIN {stg_table} AS source
            ON target.CustomerID = source.CustomerID
        WHERE target.IsCurrent = 1
        AND (
                target.CustomerEmail    <> source.CustomerEmail
            OR target.CustomerLocation <> source.CustomerLocation
        );
    """

    insert_sql = f"""
        INSERT INTO {dw_table} (
            CustomerID,
            CustomerName,
            CustomerEmail,
            CustomerLocation,
            HashID,
            StartDate,
            EndDate,
            IsCurrent
        )
        SELECT
            source.CustomerID,
            source.CustomerName,
            source.CustomerEmail,
            source.CustomerLocation,
            source.HashID,
            ?,
            NULL,
            1
        FROM {stg_table} AS source
        LEFT JOIN {dw_table} AS target
            ON target.CustomerID = source.CustomerID
        WHERE target.CustomerID IS NULL
        OR (
                target.CustomerEmail    <> source.CustomerEmail
            OR target.CustomerLocation <> source.CustomerLocation
        );
    """

    try: 
        cursor.execute(update_sql, load_date)
        cursor.execute(insert_sql, load_date)

        conn.commit()
        logger.info("Upsert task completed")

        count_inserted_sql = f"""
            SELECT COUNT(*) AS inserted_count
            FROM {dw_table}
            WHERE StartDate = ? AND IsCurrent = 1;
        """
        cursor.execute(count_inserted_sql, load_date)
        inserted_rows = cursor.fetchone()[0]
        logger.info(f"{inserted_rows} records inserted!")

        count_updated_sql = f"""
            SELECT COUNT(*) AS updated_count
            FROM {dw_table}
            WHERE EndDate = ? AND IsCurrent = 0;
        """
        cursor.execute(count_updated_sql, load_date)
        updated_rows = cursor.fetchone()[0]
        logger.info(f"{updated_rows} records updated!")

    except Exception as e:
        conn.rollback()
        logger.error(f"Failure during the upsert. Rolling back... Error detail: {e}")

    finally:
        cursor.close()
        conn.close()
