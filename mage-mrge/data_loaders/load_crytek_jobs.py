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
    i = 0
    dl = []
    base_url = "https://www.crytek.com/api/v1/lever-postings"
    logger.info(f"Requesting {base_url}")
    r = requests.get(base_url)
    rd = r.json()
    jobs = rd["postings"]
    position_count = len(jobs)
    for job in jobs:
        url = f"""{base_url}/{job["alias"]}"""
        logger.debug(f"""Requesting {base_url}/{job["alias"]}""")
        j = requests.get(url)
        jd = j.json()
        data_dict = {
            "job_id": jd.get("id", "N/A"),
            "additional_plain": jd.get("additional_plain", "N/A"),
            "created_at": jd.get("created_at", "2000-01-01 00:00:00"),
            "description_plain": jd.get("description_plain", "N/A"),
            "lists": jd.get("lists", "N/A"),
            "job_title": jd.get("text", "N/A"),
            "hosted_url": jd.get("hosted_url", "N/A"),
            "apply_url": jd.get("apply_url", "N/A"),
            "commitment": jd.get("commitment", "N/A"),
            "team": jd.get("team", "N/A"),
            "job_location": jd.get("location", "N/A"),
            "date_posted": jd.get("date_posted", "2000-01-01"),
            "valid_through": jd.get("valid_through", "2000-01-01"),
            "full_response": j.text,
            "insert_ts": datetime.now().isoformat(),
        }
        logger.debug(f"""Inserting requisition_id {jd.get("id", "N/A")}""")
        dl.append(data_dict)
        i += 1

    return pd.DataFrame(dl)


@test
def test_output(output, *args) -> None:
    """
    The output is more than one row
    """
    assert len(output.index) >= 1, "The output has at least 1 row"


@test
def test_output_team_values(output, *args) -> None:
    """
    Check if company is in expected list
    """
    output_team = output["team"].tolist()
    output_team_set = set(output_team)
    expected_team_set = {
        "Hunt: Showdown",
        "CRYENGINE",
        "Crytek",
        "Crysis 4 (Working Title)",
    }
    assert output_team_set == expected_team_set, "The output's team values are expected"
