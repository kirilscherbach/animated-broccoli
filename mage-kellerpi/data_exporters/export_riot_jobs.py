from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = "public"
    table_name = "jobs_riot"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    if not df.empty:
        with Postgres.with_config(
            ConfigFileLoader(config_path, config_profile)
        ) as loader:
            loader.export(
                df,
                schema_name,
                table_name,
                index=False,
                if_exists="append",
            )
