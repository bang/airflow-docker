import json
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# A DAG represents a workflow, a collection of tasks
with DAG(
        dag_id="tf_pipeline",
        start_date=datetime(2022, 1, 1),
        schedule=None
) as dag:

    start = EmptyOperator(task_id="start", trigger_rule="all_done")
    end = EmptyOperator(task_id="end")

    @task(task_id="load")
    def load():
        print("Loading using task flow")

    @task(task_id="transform3")
    def transform3(*, ti):
        print(f"Transforming3 using task flow {ti.xcom_pull('xc')}")

    @task(task_id="transform2")
    def transform2(*, ti):
        print(f"Transforming3 using task flow {ti.xcom_pull('xc')}")

    @task(task_id="transform1")
    def transform1(*, ti):
        print(f"Transforming3 using task flow {ti.xcom_pull('xc')}")

    @task(task_id="extract3")
    def extract3(*, ti):
        json_data = '{"kind": 3,"data": "Test3"}'
        ti.xcom_push('xc',json_data)
        return json_data

    @task(task_id="extract2")
    def extract2(*, ti):
        json_data = '{"kind": 2,"data": "Test2"}'
        ti.xcom_push('xc', json_data)
        return json_data

    @task(task_id="extract1")
    def extract1(*, ti):
        json_data = '{"kind": 1,"data": "Test1"}'
        ti.xcom_push('xc', json_data)
        return json_data

    @task()
    def airflow():
        print("airflow")


    @task.branch(task_id='triage')
    def triage(*, ti):
        all_data = ti.xcom_pull('xc')
        if isinstance(all_data, str) and len(all_data) > 0:
            all_data = json.loads(all_data)

        print(f"JSONDATA: {str(all_data)}")
        transformer = {
            'kind1': 'transform1',
            'kind2': 'transform2',
            'kind3': 'transform3'
        }

        for x in all_data:
            kind = x['kind']
            yield transformer[kind]

    # Set dependencies between tasks
    start >> [extract1(), extract2(), extract3()] >> triage() >> [transform1(), transform2(), transform3()] >> load() >> end
    # start >> [extract1(), extract2(), extract3()] >> end