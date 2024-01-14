from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Scrape Riot's website
    """
    # Specify your data loading logic here
    dl = []
    page = requests.get("https://www.riotgames.com/en/work-with-us/jobs")
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find_all("li", class_="job-row job-row--body")
    for job in job_elements:
        data_dict = {
            "job_id": job.find("a", href=True)["href"].split("/")[-1],
            "title": job.find("div", class_="job-row__col job-row__col--primary").text,
            "apply_url": f"https://www.riotgames.com{job.find('a', href=True)['href']}",
            "department": job.find_all(
                "div", class_="job-row__col job-row__col--secondary"
            )[0].text,
            "company": job.find_all(
                "div", class_="job-row__col job-row__col--secondary"
            )[0].text,
            "job_location": job.find_all(
                "div", class_="job-row__col job-row__col--secondary"
            )[2].text,
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
