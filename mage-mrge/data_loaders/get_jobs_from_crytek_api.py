import io

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
    i = 0
    base_url = "https://www.crytek.com/api/v1/lever-postings"
    logger.info(f"Requesting {base_url}")
    r = requests.get(base_url)
    rd = r.json()
    jobs = rd["postings"]
    position_count = len(jobs)
    for job in jobs:
        url = f"""{base_url}/{job["alias"]}"""
        logger.info(f"""Requesting {base_url}/{job["alias"]}""")
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
            "department": jd.get("department", "N/A"),
            "job_location": jd.get("location", "N/A"),
            "team": jd.get("team", "N/A"),
            "date_posted": jd.get("date_posted", "2000-01-01"),
            "valid_through": jd.get("valid_through", "2000-01-01"),
            "full_response": j.text,
        }
        logger.info(f"""Inserting requisition_id {jd.get("id", "N/A")}""")
        query = """
        INSERT INTO jobs_crytek (
                        job_id
                    , additional_plain
                    , created_at
                    , description_plain
                    , lists
                    , job_title
                    , hosted_url
                    , apply_url
                    , commitment
                    , department
                    , job_location
                    , team
                    , date_posted
                    , valid_through
                    , full_response
                    , insert_ts)
        VALUES (
            %(job_id)s
        , %(additional_plain)s
        , %(created_at)s
        , %(description_plain)s
        , %(lists)s
        , %(job_title)s
        , %(hosted_url)s
        , %(apply_url)s
        , %(commitment)s
        , %(department)s
        , %(job_location)s
        , %(team)s
        , %(date_posted)s
        , %(valid_through)s
        , %(full_response)s
        , NOW()::timestamp
        )
        """
        cur.execute(query, data_dict)
        i += 1

    return pd.read_csv(io.StringIO(response.text), sep=",")


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
