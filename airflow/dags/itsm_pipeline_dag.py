import os
import subprocess
import pandas as pd
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago

# ✅ Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ✅ Define the DAG
dag = DAG(
    'itsm_pipeline_dag',
    default_args=default_args,
    description='ITSM Pipeline: CSV to Postgres to DBT to Extraction',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['itsm', 'csv', 'postgres', 'dbt'],
)

# ✅ Path to the CSV file
CSV_FILE_PATH = '/home/ptpnaji123/airflow/data/transformed_dataset.csv'

# ✅ Function to ingest CSV data into PostgreSQL
def ingest_csv_to_postgres(**kwargs):
    if not os.path.exists(CSV_FILE_PATH):
        raise FileNotFoundError(f"CSV file not found at {CSV_FILE_PATH}")

    df = pd.read_csv(CSV_FILE_PATH)
    print(f"✅ Successfully read CSV with {len(df)} rows")

    # ✅ Connect to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # ✅ Drop & Recreate Table
    cursor.execute("DROP TABLE IF EXISTS itsm_tickets;")
    conn.commit()

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

    # ✅ Insert data in batches
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]
        
        insert_sql = """
        INSERT INTO itsm_tickets (
            "Ticket ID", "Category", "Sub-Category", "Priority",
            "Created Date", "Resolved Date", "Status", "Assigned Group",
            "Technician", "Customer Impact", "Resolution Time (Hrs)",
            "Year", "Month", "Day"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        values_list = [tuple(row) for _, row in batch_df.iterrows()]
        cursor.executemany(insert_sql, values_list)
        conn.commit()
        print(f"✅ Inserted records {i} to {min(i+batch_size, len(df))}")

    cursor.close()
    conn.close()
    return f"✅ Successfully ingested {len(df)} records into PostgreSQL"

# ✅ Function to run DBT models
def run_dbt_models(**kwargs):
    dbt_project_dir = '/home/ptpnaji123/dbt/itsm_project'
    if not os.path.exists(dbt_project_dir):
        raise FileNotFoundError(f"DBT project directory not found at {dbt_project_dir}")

    os.chdir(dbt_project_dir)
    result = subprocess.run(['dbt', 'run'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"❌ DBT run failed: {result.stderr}")

    return "✅ DBT models ran successfully"

# ✅ Function to validate DBT models
def validate_dbt_models(**kwargs):
    dbt_project_dir = '/home/ptpnaji123/dbt/itsm_project'
    if not os.path.exists(dbt_project_dir):
        raise FileNotFoundError(f"DBT project directory not found at {dbt_project_dir}")

    os.chdir(dbt_project_dir)
    result = subprocess.run(['dbt', 'test'], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"❌ DBT validation failed: {result.stderr}")

    return "✅ DBT models validated successfully"

# ✅ Function to extract transformed data
def extract_transformed_data(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    query = "SELECT * FROM public_public.itsm_transformed LIMIT 10;"
    cursor.execute(query)

    rows = cursor.fetchall()
    print("✅ Extracted Data:", rows)  # ✅ Print to confirm extraction

    cursor.close()
    conn.close()
    return rows

# ✅ Define Tasks
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

extract_task = PythonOperator(
    task_id='extract_transformed_data',
    python_callable=extract_transformed_data,
    dag=dag,
)

# ✅ Set task dependencies
ingest_csv_task >> run_dbt_task >> validate_dbt_task >> extract_task
