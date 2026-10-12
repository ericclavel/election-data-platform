import subprocess
from datetime import date, timedelta
from pathlib import Path


RESULTS_URL_TEMPLATE = (
    "https://electionresultsfiles.sos.mn.gov/{formatted_date}/"
)

ASSET_FILENAME = "allracesbyprecinct.txt"

def get_state_general_election_date(year: int) -> date:
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


def build_url(election_date: date) -> str:
    formatted_date = election_date.strftime("%Y%m%d")

    directory_url = RESULTS_URL_TEMPLATE.format(
        formatted_date=formatted_date
    )

    url = f"{directory_url}{ASSET_FILENAME}"

    return url


def asset_exists(url: str) -> bool:
    result = subprocess.run(
        ["wget", "--spider", url],
        capture_output=True,
    )

    return result.returncode == 0



def download_file(url: str, destination_path: Path) -> None:
    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    subprocess.run(
        [
            "wget",
            url,
            "-O",
            str(destination_path),
        ],
        check=True,
    )



def build_destination_path(election_date: date) -> Path:
    return (
        Path("data/raw")
        / "minnesota_sos"
        / "state_general"
        / election_date.strftime("%Y%m%d")
        / ASSET_FILENAME
    )



def discover_election_asset(year: int) -> None:
    election_date = get_state_general_election_date(year)
    today = date.today()

    url = build_url(election_date)

    if not asset_exists(url):
        print(f"Asset not found: {url}")
        return

    print(f"Asset found: {url}")

    if today < election_date:
        print(
            f"The election date ({election_date}) has not occurred, "
            "so this asset may contain test data."
        )
        return

    destination_path = build_destination_path(election_date)

    download_file(url, destination_path)



if __name__ == "__main__":
    discover_election_asset(2024)