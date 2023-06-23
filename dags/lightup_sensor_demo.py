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
        'lightup_sensor_demo',
        catchup=False,
        default_args=default_args,
        schedule_interval='00 00 * * *') as dag:

    task_a = bash.BashOperator(
        task_id='task_a', bash_command='echo {{ dag_run.id }}')

    test_lightup_trigger_step = LightupTriggerOperator(
        task_id="test_lightup_trigger",
        workspace_id="822d8b69-8386-41f2-8fc4-117a0ef14229",
        source_id="0a77e2b7-d1ff-4ce0-bd7f-6e3d8f9b6b1e",
        table_uuids=["5ddb7c87-5ec9-4acb-afea-4028af1da962"],
        dag_run_id='{{ dag.dag_id }} + {{ run_id }}',
    )

    test_lightup_trigger_result_step = LightupTriggerResultSensor(
        result_check_func=None,
        task_id="test_lightup_trigger_result",
        workspace_id="822d8b69-8386-41f2-8fc4-117a0ef14229",
        source_id="0a77e2b7-d1ff-4ce0-bd7f-6e3d8f9b6b1e",
        table_uuids=["5ddb7c87-5ec9-4acb-afea-4028af1da962"],
        dag_run_id='{{ dag.dag_id }} + {{ run_id }}',
    )

    task_z = bash.BashOperator(
        task_id='task_z', bash_command='echo {{ dag_run.id }}')

    task_a >> test_lightup_trigger_step
    test_lightup_trigger_result_step >> task_z

    def paused_is_fine(trigger_status: dict):
        if trigger_status["status"] == "paused":
            print(f"paused_is_fine >>> returning True")
            return True
        print(f"paused_is_fine >>> returning False")
        return False

    test_lightup_trigger_result_step_paused_is_fine = LightupTriggerResultSensor(
        result_check_func=paused_is_fine,
        task_id="test_lightup_trigger_result_step_paused_is_fine",
        workspace_id="822d8b69-8386-41f2-8fc4-117a0ef14229",
        source_id="0a77e2b7-d1ff-4ce0-bd7f-6e3d8f9b6b1e",
        table_uuids=["5ddb7c87-5ec9-4acb-afea-4028af1da962"],
        dag_run_id='{{ dag.dag_id }} + {{ run_id }}',
    )

    task_z_paused_is_fine = bash.BashOperator(
        task_id='task_z_paused_is_fine', bash_command='echo {{ dag_run.id }}')

    test_lightup_trigger_result_step_paused_is_fine >> task_z_paused_is_fine
