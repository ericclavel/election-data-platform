import json
import subprocess
import hashlib
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




def local_file_exists(destination_path: Path) -> bool:
    return destination_path.is_file()




def get_remote_asset_info(url: str) -> dict:
    result = subprocess.run(
        [
            "wget",
            "--spider",
            "--server-response",
            url,
        ],
        capture_output=True,
        text=True,
    )

    etag = None
    last_modified = None
    content_length = None

    for line in result.stderr.splitlines():
        if "ETag:" in line:
            etag = line.split("ETag:", 1)[1].strip()

        if "Last-Modified:" in line:
            last_modified = line.split("Last-Modified:", 1)[1].strip()

        if "Content-Length:" in line:
            content_length = line.split("Content-Length:", 1)[1].strip()

    return {
        "etag": etag,
        "last_modified": last_modified,
        "content_length": int(content_length) if content_length is not None else None,
    }





def build_metadata_path(election_date: date) -> Path:
    return (
        Path("data/metadata")
        / "minnesota_sos"
        / "state_general"
        / election_date.strftime("%Y%m%d")
        / "data.json"
    )




def save_metadata(election_date: date, metadata: dict) -> None:
    metadata_path = build_metadata_path(election_date)

    metadata_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with metadata_path.open("w") as file:
        json.dump(metadata, file, indent=4)




def load_metadata(election_date: date) -> dict:
    metadata_path = build_metadata_path(election_date)

    if not metadata_path.is_file():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_path}"
        )

    with metadata_path.open("r") as file:
        metadata = json.load(file)

    return metadata



def test_load_metadata(election_date: date) -> None:
    try:
        metadata = load_metadata(election_date)
        print(f"Metadata loaded successfully for {election_date}:")
        print(json.dumps(metadata, indent=4))
    except FileNotFoundError as e:
        print(str(e))



def remote_asset_has_changed(
    remote_metadata: dict,
    local_metadata: dict,
) -> bool:
    remote_fields = (
        "etag",
        "last_modified",
        "content_length",
    )

    for field in remote_fields:
        if remote_metadata.get(field) != local_metadata.get(field):
            return True

    return False



def compute_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()




def download_file(url: str, destination_path: Path) -> None:
    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_path = destination_path.with_suffix(
        destination_path.suffix + ".part"
    )

    subprocess.run(
        [
            "wget",
            url,
            "-O",
            str(temp_path),
        ],
        check=True,
    )

    temp_path.replace(destination_path)




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

    remote_metadata = get_remote_asset_info(url)

    if local_file_exists(destination_path):
        try:
            local_metadata = load_metadata(election_date)

        except FileNotFoundError:
            print(
                "Local asset exists, but metadata is missing. "
                "Re-downloading asset."
            )

        else:
            if remote_asset_has_changed(
                remote_metadata,
                local_metadata,
            ):
                print("Remote asset has changed.")
            else:
                print("Remote asset has not changed.")
                return

    download_file(url, destination_path)

    local_checksum = compute_sha256(destination_path)

    metadata = {
        **remote_metadata,
        "local_checksum_type": "SHA256",
        "local_checksum": local_checksum,
    }

    save_metadata(
        election_date,
        metadata,
    )



if __name__ == "__main__":
    discover_election_asset(2024)