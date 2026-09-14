from pathlib import Path
from urllib.parse import urlencode
from dotenv import load_dotenv
import urllib.request
import urllib.error
import json
import hashlib
from datetime import datetime, timezone
import os
import logging

load_dotenv()

FILE_PREFIX = "countypres_"
CURRENT_METADATA_PATH = Path(
    "data/metadata/mit_election_lab/county_presidential/current.json"
)
RAW_DATA_DIR = Path("data/raw/mit_election_lab/county_presidential")
DATAVERSE_BASE_URL = "https://dataverse.harvard.edu"
DATASET_DOI = "doi:10.7910/DVN/VOQCHQ"
API_TOKEN = os.environ.get("DATAVERSE_API_TOKEN")

def validate_config():
    if not API_TOKEN:
        raise ValueError(
            "DATAVERSE_API_TOKEN environment variable is not set."
        )

    
def build_metadata_url(dataset_doi):
    params = {
        "persistentId": dataset_doi,
        "excludeFiles": "false",
    }

    return (
        f"{DATAVERSE_BASE_URL}/api/datasets/:persistentId/versions/:latest-published"
        f"?{urlencode(params)}"
    )


def fetch_dataset_metadata(url, api_token):
    request = urllib.request.Request(
        url,
        headers={
            "X-Dataverse-key": api_token,
            "User-Agent": "election-data-platform/1.0",
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Dataverse metadata request failed "
            f"(HTTP {error.code}): {error_body}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Dataverse: {error.reason}"
        ) from error

    return metadata



def get_remote_source_info(metadata, file_prefix):
    dataset_info = metadata.get("data", {})
    files_info = dataset_info.get("files", [])

    dataset_version = (
        f"{dataset_info.get('versionNumber')}."
        f"{dataset_info.get('versionMinorNumber')}"
    )

    for file_info in files_info:
        data_file = file_info.get("dataFile", {})
        file_name = data_file.get("originalFileName", "")

        if file_name.startswith(file_prefix):
            return {
                "dataset_version": dataset_version,
                "file_id": data_file.get("id"),
                "file_name": file_name,
                "file_size": data_file.get("originalFileSize"),
                "dataverse_checksum_type": data_file.get("checksum", {}).get("type"),
                "dataverse_checksum": data_file.get("checksum", {}).get("value"),
            }

    raise ValueError(
        f"No source file found with prefix: {file_prefix}"
    )



def load_current_metadata(path):
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)



def source_has_changed(remote, current):
    if not current:
        logging.info("Change detected: no current metadata.")
        return True

    if remote["file_name"] != current.get("file_name"):
        logging.info("Change detected: file_name")
        return True

    if remote["dataset_version"] != current.get("dataset_version"):
        logging.info(
            "Change detected: dataset_version (%s -> %s)",
            current.get("dataset_version"),
            remote["dataset_version"],
        )
        return True

    if remote["file_id"] != current.get("file_id"):
        logging.info("Change detected: file_id")
        return True

    if remote["dataverse_checksum_type"] != current.get("dataverse_checksum_type"):
        logging.info("Change detected: dataverse_checksum_type")
        return True

    if remote["dataverse_checksum"] != current.get("dataverse_checksum"):
        logging.info("Change detected: dataverse_checksum")
        return True

    return False



def request_signed_url(file_id, api_token):
    url = (
        f"{DATAVERSE_BASE_URL}/api/access/datafile/{file_id}"
        "?format=original"
    )

    payload = {
        "guestbookResponse": {
            "answers": []
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "X-Dataverse-key": api_token,
            "Content-Type": "application/json",
            "User-Agent": "election-data-platform/1.0",

        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            response_data = json.load(response)

        return response_data["data"]["signedUrl"]

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Signed URL request failed "
            f"(HTTP {error.code}): {error_body}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Dataverse: {error.reason}"
        ) from error

    

def build_destination_path(dataset_version, file_name):
    return RAW_DATA_DIR / dataset_version / file_name


def validate_download(path, expected_size):
    if not path.exists():
        raise FileNotFoundError(
            f"Downloaded file does not exist: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Download path is not a file: {path}"
        )

    actual_size = path.stat().st_size

    if actual_size == 0:
        raise ValueError(
            f"Downloaded file is empty: {path}"
        )

    if expected_size is not None and actual_size != expected_size:
        raise ValueError(
            f"Downloaded file size mismatch: "
            f"expected {expected_size} bytes, got {actual_size} bytes."
        )


def calculate_md5(path):
    md5_hash = hashlib.md5()

    with path.open("rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()


def validate_checksum(path, expected_checksum):
    actual_checksum = calculate_md5(path)

    if actual_checksum != expected_checksum:
        raise ValueError(
            f"Checksum mismatch: "
            f"expected {expected_checksum}, got {actual_checksum}"
        )


    
def download_file(signed_url, destination_path):
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = destination_path.with_suffix(
        destination_path.suffix + ".part"
    )

    request = urllib.request.Request(
        signed_url,
        headers={
            "User-Agent": "election-data-platform/1.0",
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            with temp_path.open("wb") as file:
                file.write(response.read())

        temp_path.replace(destination_path)

    except urllib.error.HTTPError as error:
        temp_path.unlink(missing_ok=True)

        error_body = error.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"File download failed "
            f"(HTTP {error.code}): {error_body}"
        ) from error

    except urllib.error.URLError as error:
        temp_path.unlink(missing_ok=True)

        raise RuntimeError(
            f"Could not connect to Dataverse: {error.reason}"
        ) from error

    except OSError as error:
        temp_path.unlink(missing_ok=True)

        raise RuntimeError(
            f"Could not write downloaded file to {destination_path}: {error}"
        ) from error



def calculate_sha256(path):
    sha256_hash = hashlib.sha256()

    with path.open("rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()



def save_current_metadata(path, metadata):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )



def main():
    configure_logging()
    validate_config()

    dataverse_api_url = build_metadata_url(DATASET_DOI)


    metadata = fetch_dataset_metadata(
        dataverse_api_url,
        API_TOKEN
    )

    remote_source_info = get_remote_source_info(
        metadata,
        FILE_PREFIX
    )


    current_metadata = load_current_metadata(
        CURRENT_METADATA_PATH
    )

    if source_has_changed(remote_source_info, current_metadata):
        logging.info("Source has changed. Proceeding with ingestion.")
        
    else:
        logging.info("Source has not changed. No ingestion needed.")
        return

    signed_url = request_signed_url(
        remote_source_info["file_id"],
        API_TOKEN
    )

    destination_path = build_destination_path(
        remote_source_info["dataset_version"],
        remote_source_info["file_name"]
    )

    download_file(
        signed_url,
        destination_path
    )

    logging.info("Validating downloaded file...")
    validate_download(
    destination_path,
    remote_source_info["file_size"]
    )
    logging.info("Downloaded file validation passed.")

    logging.info("Validating Dataversechecksum...")
    validate_checksum(
        destination_path,
        remote_source_info["dataverse_checksum"]
    )
    logging.info("Dataverse checksum validation passed.")
    local_checksum = calculate_sha256(destination_path)

    new_current_metadata = {
        "dataset_doi": DATASET_DOI,
        "dataset_version": remote_source_info["dataset_version"],
        "file_id": remote_source_info["file_id"],
        "file_name": remote_source_info["file_name"],
        "dataverse_checksum_type": remote_source_info["dataverse_checksum_type"],
        "dataverse_checksum": remote_source_info["dataverse_checksum"],
        "local_checksum_type": "SHA256",
        "local_checksum": local_checksum,
        "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    save_current_metadata(
        CURRENT_METADATA_PATH,
        new_current_metadata
    )

if __name__ == "__main__":
    main()



