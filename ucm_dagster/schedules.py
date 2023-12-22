"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster import ScheduleDefinition
from dagster_dbt import build_schedule_from_dbt_selection
from .jobs import spendesk
'''

'''
spendesk_refresh = ScheduleDefinition(job=spendesk, cron_schedule="0 0 * * *")

schedules = [
    spendesk_refresh
#     build_schedule_from_dbt_selection(
#         [ucm_dbt_assets],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     ),
]

