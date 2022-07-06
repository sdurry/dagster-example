from dagster import job, schedule
from dagster_airbyte import airbyte_resource, airbyte_sync_op
from dagster_dbt import dbt_cloud_resource, dbt_cloud_run_op

extract_load_data = airbyte_sync_op.configured(
    {"connection_id": "<YOUR_AIRBYTE_CONNECTION_ID_HERE>"}, name="extract_load_data"
)

transform_data = dbt_cloud_run_op.configured(
    {"job_id": 54321}, name="transform_data"
)

@job(
    resource_defs={
        "airbyte": airbyte_resource.configured(
            {"host": "localhost", "port": "8000"}
        ),
        "dbt_cloud": dbt_cloud_resource.configured(
            {"auth_token": "DBT_CLOUD_AUTH_TOKEN", "account_id": 77777}
        ),
    }
)
def extract_load_transform():
    transform_data(start_after=extract_load_data())

@schedule(cron_schedule="* * * * *", job=extract_load_transform, execution_timezone="US/Central")
def my_schedule(_context):
    return {}
