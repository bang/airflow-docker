
import textwrap
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule





with DAG(
    "cl_pipeline",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["andregarciacarneiro@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        # "retries": 1,
        # "retry_delay": timedelta(minutes=5),

    },
    description="A simple tutorial DAG",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["branch", "example"],
) as dag:

    transform1 = PythonOperator(
        task_id='transform1',
        do_xcom_push=False,
        python_callable=transform1
    )

    triage = BranchPythonOperator(
        task_id='triage',
        python_callable=triage,
    )

    extract2 = PythonOperator(
        task_id='extract2',
        python_callable=extract2
    )

    extract1 = PythonOperator(
        task_id='extract1',
        python_callable=extract1
    )

    # transform1 = EmptyOperator(task_id='transform1')
    # transform2 = EmptyOperator(task_id='transform2')
    start = EmptyOperator(task_id='start', trigger_rule=TriggerRule.ALL_DONE)
    end = EmptyOperator(task_id='end', trigger_rule=TriggerRule.ALL_DONE)

    start >> [extract1, extract2] >> triage >> [transform1, transform2] >> end
