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

Before running the ingestion script, load the environment variables into the current shell:

```bash
set -a
source .env
set +a
```

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
   Calculate SHA-256
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

`current.json` is updated only after a successful download and local checksum generation.

### Running the Ingestion Script

From the project root:

```bash
python ingestion/ingest_data.py
```

Expected result when the source has not changed:

```text
Source has not changed. No ingestion needed.
```

Example result when a change is detected:

```text
Change detected: dataset_version
Source has changed. Proceeding with ingestion.
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
