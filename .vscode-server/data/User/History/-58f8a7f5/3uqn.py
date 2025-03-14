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

    # First, drop the table if it exists to ensure we recreate it with proper column sizes
    drop_table_sql = "DROP TABLE IF EXISTS itsm_tickets;"
    cursor.execute(drop_table_sql)
    conn.commit()

    # Create table with TEXT type for columns that might contain long strings
    create_table_sql = """
    CREATE TABLE itsm_tickets (
        "Ticket ID" VARCHAR(1000) PRIMARY KEY,
        "Category" VARCHAR(1000),
        "Sub-Category" VARCHAR(1000),
        "Priority" VARCHAR(1000),
        "Created Date" VARCHAR(1000),
        "Resolved Date" VARCHAR(1000),
        "Status" VARCHAR(1000),
        "Assigned Group" VARCHAR(1000),
        "Technician" VARCHAR(1000),
        "Customer Impact" TEXT,
        "Resolution Time (Hrs)" VARCHAR(1000),
        "Year" INTEGER, 
        "Month" INTEGER, 
        "Day" INTEGER
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()

    # Insert data into the table with batch processing
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]
        
        try:
            # Prepare values for bulk insert
            values_list = []
            for _, row in batch_df.iterrows():
                row_values = []
                for col in df.columns:
                    if pd.notna(row[col]):
                        row_values.append(str(row[col]))
                    else:
                        row_values.append(None)
                values_list.append(tuple(row_values))
            
            # Use executemany for batch inserting
            insert_sql = """
            INSERT INTO itsm_tickets (
                "Ticket ID", "Category", "Sub-Category", "Priority",
                "Created Date", "Resolved Date", "Status", "Assigned Group",
                "Technician", "Customer Impact", "Resolution Time (Hrs)",
                "Year", "Month", "Day"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.executemany(insert_sql, values_list)
            conn.commit()
            print(f"Committed records {i} to {min(i+batch_size, len(df))}")
                
        except Exception as e:
            print(f"Error inserting batch starting at row {i}: {e}")
            # Find the problematic row in case of error
            for j, row in batch_df.iterrows():
                try:
                    row_values = tuple(str(row[col]) if pd.notna(row[col]) else None for col in df.columns)
                    cursor.execute(insert_sql, row_values)
                    conn.commit()
                except Exception as row_error:
                    print(f"Error at row {j}:")
                    for col in df.columns:
                        val = str(row[col]) if pd.notna(row[col]) else None
                        if val:
                            print(f"Column {col}: {val[:50] + '...' if len(val) > 50 else val} (length: {len(val) if val else 0})")
                        else:
                            print(f"Column {col}: {val}")
                    conn.rollback()
            
            # Rollback the whole batch if any error occurred
            conn.rollback()
            raise

    cursor.close()
    conn.close()

    return f"Successfully ingested {len(df)} records into PostgreSQL"

# Function to run DBT models
def run_dbt_models(**kwargs):
    dbt_project_dir = '/home/ptpnaji123/dbt/itsm_project'
    if not os.path.exists(dbt_project_dir):
        raise FileNotFoundError(f"DBT project directory not found at {dbt_project_dir}")

    os.chdir(dbt_project_dir)
    result = subprocess.run(['dbt', 'run'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"DBT run failed: {result.stderr}")

    return "DBT models ran successfully"

# Function to validate DBT models
def validate_dbt_models(**kwargs):
    dbt_project_dir = '/home/ptpnaji123/dbt/itsm_project'
    if not os.path.exists(dbt_project_dir):
        raise FileNotFoundError(f"DBT project directory not found at {dbt_project_dir}")

    os.chdir(dbt_project_dir)
    result = subprocess.run(['dbt', 'test'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"DBT validation failed: {result.stderr}")

    return "DBT models validated successfully"

# Define the tasks
ingest_csv_task = PythonOperator(
    task_id='ingest_csv_to_postgres',
    python_callable=ingest_csv_to_postgres,
    dag=dag,
)

run_dbt_task = PythonOperator(
    task_id='run_dbt_models',
    python_callable=run_dbt_models,
    dag=dag,
)

validate_dbt_task = PythonOperator(
    task_id='validate_dbt_models',
    python_callable=validate_dbt_models,
    dag=dag,
)

# Set task dependencies
ingest_csv_task >> run_dbt_task >> validate_dbt_task