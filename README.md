# ITSM Data Pipeline Project

## Overview
This project builds an **IT Service Management (ITSM) Data Pipeline** using **Apache Airflow, DBT, PostgreSQL, and Apache Superset**. The pipeline processes ITSM ticket data, transforms it for analysis, and visualizes key metrics through dashboards.

## Project Structure
```
itsm-data-pipeline/
│── airflow/                   # Contains Apache Airflow DAGs
│   ├── dags/
│   │   ├── itsm_pipeline_dag.py  # Airflow DAG file
│── dbt/                        # DBT project folder
│   ├── models/
│   │   ├── transformations.sql   # DBT SQL transformations
│   ├── profiles.yml              # DBT connection profile
│── superset/                    # Apache Superset dashboard export
│   ├── dashboard_export_20250313T091857/  
│── data/                        # Raw input data
│   ├── Sample_Data_file_for_Analysis_Jan25.csv  # Raw ITSM ticket dataset
│── notebooks/                   # Jupyter notebook for data transformation
│   ├── data_transformation_ISTM.ipynb  # Transformation logic
│── README.md                     # Project documentation
│── requirements.txt               # Dependencies
│── .gitignore                     # Ignore unnecessary files
```

## Workflow & Approach
1. **Data Ingestion:** Load ITSM ticket data from `Sample_Data_file_for_Analysis_Jan25.csv`.
2. **Data Transformation:**
   - **Jupyter Notebook (`data_transformation_ISTM.ipynb`)**
   - Cleans missing values, formats dates, and generates additional fields.
   - Produces `transformed_dataset.csv` (used for further processing).
3. **Database Integration:**
   - Load `transformed_dataset.csv` into **PostgreSQL** for structured storage.
4. **DBT Transformations:**
   - DBT processes data, creating optimized tables for analysis.
5. **Apache Airflow DAGs:**
   - Automates the data pipeline (ingestion, transformation, and validation).
6. **Data Visualization (Apache Superset):**
   - Create interactive dashboards to monitor ITSM ticket trends.
   - Charts include:
     - **Ticket Volume Trends** (Line Chart)
     - **Resolution Time Comparison** (Bar Chart)
     - **Closure Rate by Assigned Group** (Pie Chart)
     - **Ticket Backlog by Priority** (Table)

## How to Run Locally

### 1️⃣ Set Up PostgreSQL
Ensure **PostgreSQL** is running and create a database:
```bash
sudo service postgresql start
psql -U postgres -c "CREATE DATABASE itsm_db;"
```

### 2️⃣ Load Data into PostgreSQL
```bash
psql -U postgres -d itsm_db -c "\copy itsm_tickets FROM 'data/transformed_dataset.csv' WITH CSV HEADER;"
```

### 3️⃣ Run DBT Models
```bash
cd dbt/itsm_project
dbt run
```

### 4️⃣ Start Apache Airflow
```bash
cd airflow/
airflow scheduler & airflow webserver
```
Access Airflow UI at: **http://localhost:8082**

### 5️⃣ Load Superset Dashboard
```bash
superset db upgrade
superset init
superset run -p 8088 --with-threads --reload --debugger
```
Access Superset UI at: **http://localhost:8088**

### 6️⃣ Upload Dashboard JSON
- Navigate to **Data → Datasets → Upload JSON**
- Select `superset/dashboard_export_20250313T091857/`
- Click **Import**

## Assumptions
- PostgreSQL is running on `localhost:5432`.
- Apache Superset and Airflow are correctly configured.
- The Jupyter Notebook generates `transformed_dataset.csv`, which is uploaded manually to PostgreSQL.

## Contributors
- **Mohammed Naji**

---


