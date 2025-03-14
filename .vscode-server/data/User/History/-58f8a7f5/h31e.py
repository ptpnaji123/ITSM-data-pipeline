import os
import subprocess
import pandas as pd
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'itsm_pipeline_dag',
    default_args=default_args,
    description='ITSM Pipeline: CSV to Postgres to DBT',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['itsm', 'csv', 'postgres', 'dbt'],
)

# Path to the CSV file
CSV_FILE_PATH = '/home/ptpnaji123/airflow/data/transformed_dataset.csv'

# Function to ingest CSV data into PostgreSQL
def ingest_csv_to_postgres(**kwargs):
    if not os.path.exists(CSV_FILE_PATH):
        raise FileNotFoundError(f"CSV file not found at {CSV_FILE_PATH}")
    
    df = pd.read_csv(CSV_FILE_PATH)
    print(f"Successfully read CSV with {len(df)} rows")
    
    # Connect to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS itsm_tickets (
        "Ticket ID" VARCHAR(1000) PRIMARY KEY,
        "Category" VARCHAR(1000),
        "Sub-Category" VARCHAR(1000),
        "Priority" VARCHAR(1000),
        "Created Date" VARCHAR(1000),
        "Resolved Date" VARCHAR(1000),
        "Status" VARCHAR(1000),
        "Assigned Group" VARCHAR(1000),
        "Technician" VARCHAR(1000),
        "Customer Impact" VARCHAR(1000),
        "Resolution Time (Hrs)" VARCHAR(1000),
        "Year" INTEGER, 
        "Month" INTEGER, 
        "Day" INTEGER
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()

    # Truncate the table before inserting new data
    cursor.execute("TRUNCATE TABLE itsm_tickets;")
    conn.commit()
    
    # Insert data into the table
    for _, row in df.iterrows():
        insert_sql = """
        INSERT INTO itsm_tickets (
            "Ticket ID", "Category", "Sub-Category", "Priority",
            "Created Date", "Resolved Date", "Status", "Assigned Group",
            "Technician", "Customer Impact", "Resolution Time (Hrs)",
            "Year", "Month", "Day"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = tuple(str(row[col]) if pd.notna(row[col]) else None for col in df.columns)
        cursor.execute(insert_sql, values)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return f"Successfully ingested {len(df)} records into PostgreSQL"

# Define the tasks
ingest_csv_task = PythonOperator(
    task_id='ingest_csv_to_postgres',
    python_callable=ingest_csv_to_postgres,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
ingest_csv_task
