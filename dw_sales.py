import logging
from datetime import datetime
from app_database import get_connection

logger = logging.getLogger('etl_logger')

def upsert_sales(stg_table: str, dw_table: str):
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
            ON target.Date = source.Date
            AND target.ProductID = source.ProductID
            AND target.CustomerID = source.CustomerID
        WHERE target.IsCurrent = 1
        AND (
                target.ProductName   <> source.ProductName OR
                target.QuantitySold  <> source.QuantitySold OR
                target.Price         <> source.Price OR
                target.Category      <> source.Category OR
                target.HashID        <> source.HashID
            );
    """

    insert_sql = f"""
        INSERT INTO {dw_table} (
            Date,
            ProductID,
            ProductName,
            QuantitySold,
            Price,
            TotalSales,
            Category,
            CustomerID,
            HashID,
            StartDate,
            EndDate,
            IsCurrent
        )
        SELECT
            source.Date,
            source.ProductID,
            source.ProductName,
            source.QuantitySold,
            source.Price,
            source.QuantitySold * source.Price AS TotalSales,
            source.Category,
            source.CustomerID,
            source.HashID,
            ?,
            NULL,
            1
        FROM {stg_table} AS source
        LEFT JOIN {dw_table} AS target
            ON target.Date = source.Date
            AND target.ProductID = source.ProductID
            AND target.CustomerID = source.CustomerID
            AND target.IsCurrent = 1
        WHERE target.CustomerID IS NULL
        OR (
                target.ProductName   <> source.ProductName OR
                target.QuantitySold  <> source.QuantitySold OR
                target.Price         <> source.Price OR
                target.Category      <> source.Category OR
                target.HashID        <> source.HashID
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

        count_updated_sql = f"""
            SELECT COUNT(*) AS updated_count
            FROM {dw_table}
            WHERE EndDate = ? AND IsCurrent = 0;
        """

        cursor.execute(count_inserted_sql, load_date)
        inserted_rows = cursor.fetchone()[0]
        logger.info(f"{inserted_rows} records inserted!")

        cursor.execute(count_updated_sql, load_date)
        updated_rows = cursor.fetchone()[0]
        logger.info(f"{updated_rows} records updated!")
        
    except Exception as e:
        conn.rollback()
        logger.info(f"Failure during the upsert. Rollbacking... Error detail: {e}")
    
    finally:
        cursor.close()
        conn.close()
