import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin
from datetime import date, timedelta

RESULTS_BASE_URL = "https://electionresultsfiles.sos.mn.gov"

RESULTS_URL_TEMPLATE = (
    "https://electionresultsfiles.sos.mn.gov/{formatted_date}/"
)


def get_state_general_election_date(year):
    if year % 2 != 0:
        raise ValueError(
            "Minnesota State General Elections occur in even-numbered years"
        )

    first_day_of_november = date(year, 11, 1)

    days_until_monday = (0 - first_day_of_november.weekday()) % 7

    first_monday = first_day_of_november + timedelta(
        days=days_until_monday
    )

    election_date = first_monday + timedelta(days=1)


    return election_date

def build_url(election_date):
    formatted_date = election_date.strftime("%Y%m%d")
    url = RESULTS_URL_TEMPLATE.format(
        formatted_date=formatted_date
    )

    return url



if __name__=="__main__":