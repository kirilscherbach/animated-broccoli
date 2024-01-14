import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def clean_str(string):
    return string.strip().replace("\n", " ")


@data_loader
def load_data(*args, **kwargs):
    """
    Scrape Riot's website
    """
    # Specify your data loading logic here
    dl = []
    page = requests.get("https://ea.gr8people.com/jobs")
    soup = BeautifulSoup(page.content, "html.parser")
    page_info = soup.find("a", rel="nofollow")
    span = page_info.find("span")
    span.extract()
    max_page = page_info.text.strip()
    for page_num in range(1, int(max_page) + 1):
        page = requests.get(f"https://ea.gr8people.com/jobs?page={page_num}")
        soup = BeautifulSoup(page.content, "html.parser")
        job_elements = soup.find(
            "tbody", id=re.compile("search-results-\d+-bodyEl")  # noqa: W605
        )
        for job in job_elements.find_all("tr"):
            data_dict = {
                "job_id": clean_str(
                    job.find_all("td", class_="search-results-column-left")[0].text
                ),
                "title": clean_str(
                    job.find_all("td", class_="search-results-column-left")[1].text
                ),
                "apply_url": job.find("a", href=True)["href"],
                "department": clean_str(
                    job.find_all("td", class_="search-results-column-left")[2].text
                ),
                "remote": clean_str(
                    job.find_all("td", class_="search-results-column-left")[4].text
                ),
                "job_location": clean_str(
                    job.find_all("td", class_="search-results-column-left")[3].text
                ),
                "insert_ts": datetime.now().isoformat(),
            }
            dl.append(data_dict)
        print(f"Finished scraping page {page_num}")

    return pd.DataFrame(dl)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
