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
    """ """
    execution_dt = kwargs["execution_date"].strftime("%Y-%m-%d")
    query = f"""
    select
        "source",
        "update_job_id",
        "job_status",
        "job_id"::text,
        "absolute_url",
        "title",
        "department",
        "company",
        "remote"::text,
        "job_location",
        "insert_date"
    from  public.jobs_crytek_daily_update where insert_date = '{execution_dt}'
    union all
    select
        "source",
        "update_job_id",
        "job_status",
        "job_id"::text,
        "absolute_url",
        "title",
        "department",
        "company",
        "remote"::text,
        "job_location",
        "insert_date"
    from  public.jobs_epic_daily_update where insert_date = '{execution_dt}'
    union all
    select
        "source",
        "update_job_id",
        "job_status",
        "job_id"::text,
        "absolute_url",
        "title",
        "department",
        "company",
        "remote"::text,
        "job_location",
        "insert_date"
    from  public.jobs_chymera_daily_update where insert_date = '{execution_dt}'
    union all
    select
        "source",
        "update_job_id",
        "job_status",
        "job_id"::text,
        "absolute_url",
        "title",
        "department",
        "company",
        "remote"::text,
        "job_location",
        "insert_date"
    from  public.jobs_riot_daily_update where insert_date = '{execution_dt}'
    union all
    select
        "source",
        "update_job_id",
        "job_status",
        "job_id"::text,
        "absolute_url",
        "title",
        "department",
        "company",
        "remote"::text,
        "job_location",
        "insert_date"
    from  public.jobs_ea_daily_update where insert_date = '{execution_dt}'
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
