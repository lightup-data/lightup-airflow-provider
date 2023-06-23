import datetime

from airflow import models
from airflow.operators import bash
from lightup_trigger_operator import LightupTriggerOperator
from lightup_trigger_result_sensor import LightupTriggerResultSensor

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'Lightup',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}

with models.DAG(
        'lightup_sensor_demo2',
        catchup=False,
        default_args=default_args,
        schedule_interval='00 00 * * *') as dag:

    task_a = bash.BashOperator(
        task_id='task_a', bash_command='echo {{ dag_run.id }}')

    test_lightup_trigger_step = LightupTriggerOperator(
        task_id="test_lightup_trigger",
        workspace_id="822d8b69-8386-41f2-8fc4-117a0ef14229",
        source_id="0a77e2b7-d1ff-4ce0-bd7f-6e3d8f9b6b1e",
        metric_uuids=["cfe5b542-8f4f-4062-88e0-4b2ab1aed3fb"],
        dag_run_id='{{ dag.dag_id }} + {{ run_id }}',
    )

    task_a >> test_lightup_trigger_step

    test_lightup_trigger_result_step = LightupTriggerResultSensor(
        task_id="test_lightup_trigger_result_step",
        workspace_id="822d8b69-8386-41f2-8fc4-117a0ef14229",
        source_id="0a77e2b7-d1ff-4ce0-bd7f-6e3d8f9b6b1e",
        metric_uuids=["cfe5b542-8f4f-4062-88e0-4b2ab1aed3fb"],
        dag_run_id='{{ dag.dag_id }} + {{ run_id }}',
    )

    task_z = bash.BashOperator(
        task_id='task_z', bash_command='echo {{ dag_run.id }}')

    test_lightup_trigger_result_step >> task_z
