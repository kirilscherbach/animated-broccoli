from datetime import datetime

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    logger = kwargs.get("logger")
    url = "https://chimera-entertainment.jobs.personio.com/search.json"
    logger.info(f"Requesting {url}")
    response = requests.get(url)

    jjobs = response.json()
    dl = []
    for jd in jjobs:
        data_dict = {
            "job_id": jd.get("id", "N/A"),
            "job_title": jd.get("name", "N/A"),
            "employment_type": jd.get("employment_type", "N/A"),
            "seniority": jd.get("seniority", "N/A"),
            "keywords": jd.get("keywords", "N/A"),
            "description": jd.get("description", "N/A"),
            "office": jd.get("office", "N/A"),
            "schedule": jd.get("schedule", "N/A"),
            "category": jd.get("category", "N/A"),
            "department": jd.get("department", "N/A"),
            "subcompany": jd.get("subcompany", "N/A"),
            "url": f"""https://chimera-entertainment.jobs.personio.com/job/{jd.get("id", "N/A")}""",
            "insert_ts": datetime.now().isoformat(),
        }
        dl.append(data_dict)

    return pd.DataFrame(dl)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
