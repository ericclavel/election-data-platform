# Election Data Platform

## Project Overview

### Goal

Build a scalable historical U.S. election data platform capable of standardizing election results across elections, offices, and changing geographic boundaries.

### V1 Scope

Presidential election results by county.

### Initial Time Range

2000–2024.

### Future Scope

* Congressional elections
* State legislative elections
* District boundary histories
* Census geography
* Redistricting analysis

## Raw Data Ingestion

### Dataverse Prerequisites

A Harvard Dataverse account is required.

The account profile must contain:

* Name
* Email
* Institution
* Position

The MIT dataset uses Dataverse Guestbook ID 458, which requires all four fields before a download request can be authorized.

### Configuration

Generate a Harvard Dataverse API token and store it in the local `.env` file:

```text
DATAVERSE_API_TOKEN=<your-token>
```

The `.env` file must not be committed to Git.


### Ingestion Workflow

```text
Dataset DOI
    ↓
Query latest published version
    ↓
Locate target source file
    ↓
Compare against current.json
    ↓
Source unchanged?
├── Yes → Exit
└── No
     ↓
   Submit guestbook request
     ↓
   Receive temporary signed URL
     ↓
   Download original CSV
     ↓
    Validate file size
     ↓
    Verify Dataverse MD5
     ↓
    Calculate local SHA-256
     ↓
    Update current.json
```

### Raw Storage

```text
data/raw/mit_election_lab/county_presidential/
└── 20.0/
    └── countypres_2000-2024.csv
```

Raw source files are stored without transformation. Schema normalization, type casting, cleaning, and other transformations occur downstream.

### Ingestion Metadata

```text
data/metadata/mit_election_lab/county_presidential/current.json
```

`current.json` records the most recent source version that was successfully downloaded and validated locally.

The ingestion process records two checksums:

* `dataverse_checksum` — checksum reported by Dataverse for the source file.
* `local_checksum` — SHA-256 calculated locally from the downloaded raw file.

Before current.json is updated, the downloaded file is validated against:

- expected file size reported by Dataverse
- MD5 checksum reported by Dataverse

After validation succeeds, the pipeline calculates a local SHA-256 fingerprint of the downloaded raw file and records it in current.json.


## Docker

Docker provides a reproducible Python environment for running the ingestion pipeline. The image contains Python, `uv`, project dependencies, and the ingestion script, while raw data and ingestion metadata remain on the host.

### Build and Run

Ensure a local `.env` file exists and contains:

```text
DATAVERSE_API_TOKEN=<your-token>
```

Run the ingestion service from the project root:

```bash
docker compose up --build ingestion
```

This builds the image when needed, starts the ingestion container, runs the ingestion script, and exits when ingestion completes.

### Ingestion Output

If the currently published Dataverse source matches the locally recorded metadata, ingestion is skipped:

```text
INFO | Source has not changed. No ingestion needed.
```

If a change is detected, the pipeline proceeds with download and validation:

```text
INFO | Change detected: dataset_version (20.0 -> 21.0)
INFO | Source has changed. Proceeding with ingestion.
INFO | Validating downloaded file...
INFO | Downloaded file validation passed.
INFO | Validating Dataverse checksum...
INFO | Dataverse checksum validation passed.
```

### Environment Variables

The Dataverse API token is stored in `.env` as `DATAVERSE_API_TOKEN` and loaded into the container at runtime through Docker Compose.

The `.env` file is excluded from the Docker build context using `.dockerignore` and is not included in the image. Required environment variables are documented in `.env.example`.

### Persistent Data

The project data directory is mounted into the container:

```yaml
volumes:
  - ./data:/code/data
```

This maps:

```text
host ./data
    ↕
container /code/data
```

Raw data and ingestion metadata therefore persist on the host outside the container:

```text
data/raw/
data/metadata/
```


## Project Structure

```text
election-data-platform/
├── data/
│   ├── raw/
│   └── metadata/
├── ingestion/
│   └── ingest_data.py
├── notebooks/
├── .env.example
└── README.md
```


