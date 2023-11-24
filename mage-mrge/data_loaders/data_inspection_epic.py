from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    date_filter = kwargs["execution_date"]
    query = f"""
        select
            to_char(insert_date, 'YYYY-MM-DD') as update_date,
            job_status,
            department,
            company,
            count(*) as count_positions
        from
            (select
                insert_date,
                job_status,
                department,
                company
            from
            jobs_epic_daily_update
            union all
            select
                insert_date,
                job_status,
                department,
                company
            from
            jobs_crytek_daily_update)
        where job_status = 'Position opened'
        and insert_date > '{date_filter}'::date - 30
        group by
            insert_date,
            job_status,
            department,
            company
        order by
            insert_date asc


    """

    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "reader"

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
