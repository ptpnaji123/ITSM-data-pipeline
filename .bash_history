whoami  # Shows your UNIX username
ls ~    # Lists your home directory
docker --version
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip -y
ls ~/airflow
mkdir ~/airflow && cd ~/airflow
python3 -m venv airflow-env
source airflow-env/bin/activate
pip install apache-airflow
export AIRFLOW_HOME=~/airflow
airflow db init
airflow webserver --port 8080
airflow webserver --port 8081
airflow users create     --username admin     --firstname Mohammed     --lastname Naji     --role Admin     --email ptpnaji123@gmail.com
airflow webserver --port 8081
pip install apache-airflow-providers-postgres
airflow webserver --port 8081
cd ~/airflow/dags
mkdir -p ~/airflow/dags
cd ~/airflow/dags
nano itsm_pipeline_dag.py
airflow scheduler &
airflow webserver --port 8081
pip install apache-airflow-providers-postgres
pip list | grep apache-airflow-providers-postgres
airflow scheduler &
airflow webserver --port 8081
python -c 'from airflow.providers.postgres.operators.postgres import PostgresOperator; print("Success!")'
source ~/airflow/airflow-env/bin/activate
pip install apache-airflow-providers-postgres --upgrade
pip list | grep apache-airflow-providers-postgres
pkill -f "airflow"
airflow scheduler &
airflow webserver --port 8081
source ~/airflow/airflow-env/bin/activate
pip install --no-cache-dir --upgrade apache-airflow-providers-postgres
pip list | grep apache-airflow-providers-postgres
airflow scheduler &
airflow webserver --port 8081
airflow version
pip list | grep apache-airflow-providers-postgres
python -c "import airflow.providers.postgres.operators.postgres; print('Import successful')"
pip install apache-airflow-providers-postgres==2.10.5
python -c "import airflow.providers.postgres.operators.postgres; print('Import successful')"
airflow providers list
python -c "import airflow.providers.postgres; print(dir(airflow.providers.postgres))"
python -c "import airflow.providers.postgres; from pathlib import Path; print(list(Path(airflow.providers.postgres.__file__).parent.glob('*')))"
pip uninstall -y apache-airflow-providers-postgres
pip install apache-airflow-providers-postgres==5.4.0
python -c "import airflow.providers.postgres; from pathlib import Path; print(list(Path(airflow.providers.postgres.__file__).parent.glob('*')))"
python -c "import airflow.providers.postgres.operators; print(dir(airflow.providers.postgres.operators))"
python -c "from pathlib import Path; import airflow.providers.postgres.operators; print(list(Path(airflow.providers.postgres.operators.__file__).parent.glob('*')))"
python -c "from airflow.providers.postgres.operators.postgres import PostgresOperator; print('Import successful')"
pkill -f "airflow webserver"
pkill -f "airflow scheduler"
airflow webserver -p 8081 -D
airflow scheduler -D
airflow scheduler &
airflow webserver --port 8081
pip install pandas
ps aux | grep airflow
kill -9 8191  # The PID shown in your error
rm /home/ptpnaji123/airflow/airflow-webserver.pid
airflow webserver --port 8081
sudo lsof -i :8081
sudo kill -9 <PID>
sudo fuser -k 8081/tcp
netstat -tuln | grep 8081
ps aux | grep airflow
sudo apt install net-tools
netstat -tuln | grep 8081
pkill -f airflow
airflow scheduler -D
airflow webserver --port 8082 -D
cd ~/airflow/dags
ls -l ~/airflow/dags/
nano ~/airflow/dags/itsm_pipeline_dag.py
airflow webserver --port 8082 -D
scp transformed_dataset.csv ptpnaji123@your-server:/home/ptpnaji123/airflow/data/
scp d:ITSM/transformed_dataset.csv ptpnaji123@your-server:/home/ptpnaji123/airflow/data/
sudo mkdir /mnt/d
mkdir -p ~/airflow/data
cp /mnt/d/ITSM/transformed_dataset.csv ~/airflow/data/
CSV_FILE_PATH = '/home/ptpnaji123/airflow/data/transformed_dataset.csv'
ls -la /mnt/d/ITSM/
nano ~/airflow/dags/itsm_pipeline_dag.py
airflow webserver --port 8082 -D
cat ~/airflow/dags/itsm_pipeline_dag.py | grep CSV_FILE_PATH
nano ~/airflow/dags/itsm_pipeline_dag.py
cat ~/airflow/dags/itsm_pipeline_dag.py | grep CSV_FILE_PATH
ls -la /home/ptpnaji123/airflow/data/transformed_dataset.csv
nano ~/airflow/dags/itsm_pipeline_dag.py
airflow webserver --port 8082 -D
sudo lsof -i :8081
airflow connections get postgres_default
airflow connections delete postgres_default
airflow connections add 'postgres_default'     --conn-type 'postgres'     --conn-host 'localhost'     --conn-schema 'airflow'     --conn-login 'postgres'     --conn-password 'airflow'     --conn-port '8081'
airflow webserver --port 8082 -D
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo netstat -tulnp | grep postgres
sudo netstat -tulnp | grep 5432
ss -tulnp | grep 5432
sudo netstat -tulnp | grep 8082
sudo netstat -tulnp | grep 5432
sudo netstat -tulnp | grep 8082
tcp        0      0 0.0.0.0:8082            0.0.0.0:*               LISTEN      8998/gunicorn: mastsudo netstat -tulnp | grep 8082
sudo netstat -tulnp | grep 5432
sudo netstat -tulnp | grep 8081
sudo netstat -tulnp | grep 5432
ss -tulnp | grep 5432
sudo service postgresql start
sudo service postgresql status
sudo nano /etc/postgresql/15/main/postgresql.conf
tcp        0      0 0.0.0.0:8082
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ sudo netstat -tulnp | grep 5432
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ sudo netstat -tulnp | grep 8081
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ sudo netstat -tulnp | grep 5432
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ ss -tulnp | grep 5432
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ sudo service postgresql start
Failed to start postgresql.service: Unit postgresql.service not found.
(airflow-env) ptpnaji123@DESKTOP-KFL7LN6:~/airflow/dags$ sudo service postgresql status
Unit postgresql.service could not be found.
psql --version
sudo apt install postgresql-client-common
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
sudo service postgresql status
sudo netstat -tulnp | grep 5432
sudo -u postgres psql
wsl
airflow scheduler &
airflow webserver --port 8082
sudo netstat -tulnp | grep 5432
airflow connections add postgres_default     --conn-type postgres     --conn-host localhost     --conn-schema postgres     --conn-login postgres     --conn-password YOUR_PASSWORD     --conn-port 5432
airflow connections delete postgres_default
airflow connections add postgres_default     --conn-type postgres     --conn-host localhost     --conn-schema postgres     --conn-login postgres     --conn-password 8606559447\ 
airflow scheduler &
airflow webserver --port 8082 &
airflow connections delete postgres_default
airflow connections add postgres_default     --conn-type postgres     --conn-host localhost     --conn-schema postgres     --conn-login postgres     --conn-password ptpnaji123\ 
airflow webserver --port 8082 
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD '8606559447'; 
\q
airflow connections delete postgres_default
airflow connections add postgres_default     --conn-type postgres     --conn-host localhost     --conn-schema postgres     --conn-login postgres     --conn-password 8606559447\ 
airflow scheduler &
airflow webserver --port 8082 &
sudo -u postgres psql
airflow connections delete postgres_default
airflow connections add postgres_default     --conn-type postgres     --conn-host localhost     --conn-schema postgres     --conn-login postgres     --conn-password ptpnaji123     --conn-port 5432
sudo service postgresql restart
airflow scheduler &
airflow webserver --port 8082 &
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'your_table_name';
psql -U postgres -d your_database
nano modify_table.sql
nano ~/airflow/dags/itsm_pipeline_dag.py
airflow webserver --port 8082 
airflow scheduler stop
airflow webserver stop
wsl --shutdown
