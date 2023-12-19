"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster import ScheduleDefinition
from dagster_dbt import build_schedule_from_dbt_selection
from .jobs import update_spendesk_api_key

spendesk_api_refresh_job = ScheduleDefinition(job=update_spendesk_api_key, cron_schedule="0 0 * * *")

schedules = [
    spendesk_api_refresh_job
#     build_schedule_from_dbt_selection(
#         [ucm_dbt_assets],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     ),
]

