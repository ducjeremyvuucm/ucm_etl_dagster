from dagster import EnvVar
from dagster_airbyte import AirbyteResource

airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    # If using basic auth, include username and password:
    username="airbyte",
    password=EnvVar("AIRBYTE_PASSWORD"),
)
