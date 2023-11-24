import math
from datetime import datetime

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def get_total_hits_and_page_size(url, params):
    r = requests.get(url, params)
    rd = r.json()
    total_hits = rd["total"]
    page_size = len(rd["hits"])
    return total_hits, page_size


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    load jobs from epic api
    """
    logger = kwargs.get("logger")
    base_url = (
        "http://mw-greenhouse-service-prod.debc.live.use1a.on.epicgames.com/api/job"
    )
    params = {"keyword": "data", "skip": 0}
    dl = []
    skip = 0
    page = 1
    position_count, page_size = get_total_hits_and_page_size(base_url, params)
    logger.info(f"There are {position_count} hits, with page size of {page_size}")
    page_count = math.ceil(position_count / page_size)
    logger.info(f"There are {page_count} total pages")
    for i in range(1, page_count + 1):
        params = {"keyword": "data", "skip": skip}
        logger.info(f"Requesting page {i}")
        r = requests.get(base_url, params)
        logger.info(f"Requested {r.url}")
        rd = r.json()
        for hit in rd["hits"]:
            r_position = requests.get(url=f"""{base_url}/{hit["id"]}""")
            rd_position = r_position.json()
            logger.debug(
                f"""Inserting requisition_id {rd_position.get("requisition_id", "N/A")}"""
            )
            data_dict = {
                "absolute_url": rd_position.get("absolute_url", "N/A"),
                "education": rd_position.get("education", "N/A"),
                "internal_job_id": rd_position.get("internal_job_id", "N/A"),
                "requisition_id": rd_position.get("requisition_id", "N/A"),
                "title": rd_position.get("title", "N/A"),
                "content": rd_position.get("content", "N/A"),
                "department": rd_position.get("department", "N/A"),
                "company": rd_position.get("company", "N/A"),
                "remote": rd_position.get("remote", "N/A"),
                "spotlight": rd_position.get("spotlight", "N/A"),
                "type": rd_position.get("type", "N/A"),
                "city": rd_position.get("city", "N/A"),
                "state": rd_position.get("state", "N/A"),
                "country": rd_position.get("country", "N/A"),
                "filterText": rd_position.get("filterText", "N/A"),
                "updated_at": rd_position.get("updated_at", "2000-01-01 00:00:00"),
                "full_response": r_position.text,
                "insert_ts": datetime.now().isoformat(),
            }
            dl.append(data_dict)
            skip += 1

    return pd.DataFrame(dl)


@test
def test_output_length(output, *args) -> None:
    """
    Check if output has more than one row
    """
    assert len(output.index) >= 1, "The output has at least 1 row"


@test
def test_output_company_values(output, *args) -> None:
    """
    Check if company is in expected list
    """
    output_companies = output["company"].tolist()
    output_companies_set = set(output_companies)
    expected_companies_set = {"Epic Games", "Harmonix", "Psyonix"}
    assert (
        output_companies_set == expected_companies_set
    ), "The output's companies values are expected"
