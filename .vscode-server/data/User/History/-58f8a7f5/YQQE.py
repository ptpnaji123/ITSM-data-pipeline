DESKTOP-KFL7LN6.
 ▶ Log message source details
[2025-03-13, 09:11:45 UTC] {local_task_job_runner.py:123} ▶ Pre task execution logs
[2025-03-13, 09:11:50 UTC] {logging_mixin.py:190} INFO - Successfully read CSV with 1870 rows
[2025-03-13, 09:11:50 UTC] {base.py:84} INFO - Retrieving connection 'postgres_default'
[2025-03-13, 09:11:50 UTC] {sql.py:248} WARNING - This setter is for backward compatibility and should not be used.
Since the introduction of connection property, the providers listed below breaks due to assigning value to self.connection in their __init__ method.
* apache-airflow-providers-mysql<5.7.1
* apache-airflow-providers-elasticsearch<5.5.1
* apache-airflow-providers-postgres<5.13.0
[2025-03-13, 09:11:52 UTC] {taskinstance.py:3313} ERROR - Task failed with exception
Traceback (most recent call last):
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/models/taskinstance.py", line 768, in _execute_task
    result = _execute_callable(context=context, **execute_callable_kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/models/taskinstance.py", line 734, in _execute_callable
    return ExecutionCallableRunner(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/utils/operator_helpers.py", line 252, in run
    return self.func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/models/baseoperator.py", line 424, in wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/operators/python.py", line 238, in execute
    return_value = self.execute_callable()
                   ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/operators/python.py", line 256, in execute_callable
    return runner.run(*self.op_args, **self.op_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/airflow-env/lib/python3.12/site-packages/airflow/utils/operator_helpers.py", line 252, in run
    return self.func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ptpnaji123/airflow/dags/itsm_pipeline_dag.py", line 84, in ingest_csv_to_postgres
    cursor.execute(insert_sql, values)
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(255)
[2025-03-13, 09:11:52 UTC] {logging_mixin.py:190} INFO - Task instance in failure state
[2025-03-13, 09:11:52 UTC] {logging_mixin.py:190} INFO - Task start:2025-03-13 09:11:46.061449+00:00 end:2025-03-13 09:11:52.204007+00:00 duration:6.142558
[2025-03-13, 09:11:52 UTC] {logging_mixin.py:190} INFO - Task:<Task(PythonOperator): ingest_csv_to_postgres> dag:<DAG: itsm_pipeline_dag> dagrun:<DagRun itsm_pipeline_dag @ 2025-03-13 09:11:36.569382+00:00: manual__2025-03-13T09:11:36.569382+00:00, state:running, queued_at: 2025-03-13 09:11:36.620797+00:00. externally triggered: True>
[2025-03-13, 09:11:52 UTC] {logging_mixin.py:190} INFO - Failure caused by value too long for type character varying(255)
[2025-03-13, 09:11:52 UTC] {taskinstance.py:1226} INFO - Marking task as UP_FOR_RETRY. dag_id=itsm_pipeline_dag, task_id=ingest_csv_to_postgres, run_id=manual__2025-03-13T09:11:36.569382+00:00, execution_date=20250313T091136, start_date=20250313T091146, end_date=20250313T091152
[2025-03-13, 09:11:52 UTC] {taskinstance.py:341} ▶ Post task execution logs