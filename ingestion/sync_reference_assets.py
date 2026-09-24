from pathlib import Path
from urllib.parse import urlencode
from dotenv import load_dotenv
from config import DATASETS

import urllib.request
import urllib.error
import json
import hashlib
from datetime import datetime, timezone
import os
import logging

load_dotenv()

DATAVERSE_BASE_URL = "https://dataverse.harvard.edu"
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



def get_remote_reference_info(metadata, reference_asset):
    dataset_info = metadata.get("data", {})
    files_info = dataset_info.get("files", [])

    dataset_version = (
        f"{dataset_info.get('versionNumber')}."
        f"{dataset_info.get('versionMinorNumber')}"
    )

    for file_info in files_info:
        data_file = file_info.get("dataFile", {})
        file_name = (
            data_file.get("originalFileName", "")
            or file_info.get("label")
        )

        if reference_asset.match_field == "label":
            match_value = file_info.get("label", "")

        elif reference_asset.match_field == "originalFileName":
            match_value = data_file.get("originalFileName") or ""

        if match_value.startswith(reference_asset.file_prefix):
            return {
                "dataset_version": dataset_version,
                "file_id": data_file.get("id"),
                "file_name": file_name,
                "file_size": data_file.get("originalFileSize"),
                "dataverse_checksum_type": data_file.get("checksum", {}).get("type"),
                "dataverse_checksum": data_file.get("checksum", {}).get("value"),
            }



##for reference_asset in config.reference_assets:
    remote_reference_info = get_remote_reference_info(
        metadata,
        reference_asset,
    )