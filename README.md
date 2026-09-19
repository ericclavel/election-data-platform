# Election Data Platform

## Project Overview

### Goal

Build a scalable historical U.S. election data platform capable of ingesting, validating, standardizing, and analyzing election results across election types, offices, and changing geographic boundaries.

### Project Status

The platform is currently in the source-ingestion and discovery phase.

Implemented:

* Reproducible source ingestion
* Source-version detection
* Raw-file preservation
* File-size and upstream checksum validation
* Local SHA-256 fingerprinting
* Persistent ingestion metadata
* Docker-based execution
* Dataset-level source, schema, and data-quality documentation

Not yet implemented:

* Shared multi-source ingestion configuration
* Analytical storage
* Staging and transformation models
* Cross-dataset standardization
* Geographic boundary integration
* Analytical or serving layers

### Planned Scope

The platform is intended to support multiple election and geographic datasets, including:

* Presidential elections
* U.S. congressional elections
* State legislative elections
* Precinct-level election results
* District boundary histories
* Census geography
* Redistricting analysis

## Data Sources

Dataset-specific documentation is maintained under `docs/sources/`.

Each dataset directory contains:

* `README.md` — source identity, provenance, coverage, storage, and ingestion notes
* `source_schema.md` — raw schema and structural observations
* `data_quality_findings.md` — source-specific quality findings and unresolved issues

Current source documentation:

* [County Presidential Election Returns](docs/sources/mit_election_lab/county_presidential/README.md)
* [U.S. House Election Returns](docs/sources/mit_election_lab/us_house/README.md)

Reusable dataset documentation templates are maintained under:

```text
docs/templates/dataset/
```

## Raw Data Ingestion

### Ingestion Principles

The ingestion layer is responsible for acquiring and validating source data while preserving original source files without transformation.

Schema normalization, type casting, cleaning, harmonization, and analytical modeling occur downstream.

Detailed ingestion behavior, validation rules, logging, failure handling, and source-change detection are documented in the [Ingestion README](ingestion/README.md).

### General Ingestion Workflow

```text
Configured source
      ↓
Query current published source metadata
      ↓
Locate target source file
      ↓
Compare against locally recorded metadata
      ↓
Source unchanged?
├── Yes → Exit
└── No
     ↓
Acquire original source file
     ↓
Validate downloaded file
     ↓
Verify upstream checksum
     ↓
Calculate local SHA-256 fingerprint
     ↓
Persist raw source
     ↓
Update local ingestion metadata
```

Source-specific access requirements and ingestion behavior are documented in each dataset README.

### Raw Storage

Raw source files are organized by source organization, dataset, and upstream dataset version:

```text
data/raw/
└── <source>/
    └── <dataset>/
        └── <dataset_version>/
            └── <source_file>
```

Raw files are preserved without transformation.

### Ingestion Metadata

Successful ingestion state is recorded separately from raw source data:

```text
data/metadata/
└── <source>/
    └── <dataset>/
        └── current.json
```

`current.json` represents the most recent source version successfully downloaded and validated locally.

The ingestion process records both:

* the checksum reported by the upstream source
* a local SHA-256 fingerprint calculated from the downloaded file

Local ingestion metadata is updated only after required validation succeeds.

## Docker

Docker provides the reproducible execution environment for the platform.

Application dependencies are contained within Docker images, while raw data and ingestion metadata remain outside disposable containers.

### Prerequisites

* Git
* Docker
* Docker Compose
* Required credentials for configured data sources

Development is currently performed using WSL2/Ubuntu on Windows, but WSL is not intended to be a platform requirement.

### Configuration

Create a local `.env` file from the provided example:

```bash
cp .env.example .env
```

Populate the required source credentials documented in `.env.example`.

The `.env` file must not be committed to Git.

It is excluded from the Docker build context using `.dockerignore` and supplied to containers only at runtime.

### Build and Run

From the project root:

```bash
docker compose up --build ingestion
```

This is the platform-level entry point for raw-data ingestion.

As additional sources are integrated, the ingestion implementation may expand while preserving this top-level execution workflow.

### Persistent Data

The project data directory is mounted into the ingestion environment:

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

Raw data and ingestion metadata therefore persist independently of container lifecycle:

```text
data/raw/
data/metadata/
```

## Project Structure

```text
election-data-platform/
├── data/
│   ├── raw/
│   │   └── <source>/
│   │       └── <dataset>/
│   │           └── <dataset_version>/
│   │               └── <source_file>
│   │
│   └── metadata/
│       └── <source>/
│           └── <dataset>/
│               └── current.json
│
├── docs/
│   ├── sources/
│   │   └── <source>/
│   │       └── <dataset>/
│   │           ├── README.md
│   │           ├── source_schema.md
│   │           └── data_quality_findings.md
│   │
│   └── templates/
│       └── dataset/
│           ├── README.md
│           ├── source_schema.md
│           └── data_quality_findings.md
│
├── ingestion/
│   ├── config.py
│   ├── ingest_data.py
│   └── README.md
│
├── notebooks/
│
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Development Approach

The platform is being developed incrementally.

New data sources are inspected and documented before downstream abstractions are introduced. Shared ingestion, staging, and modeling patterns are generalized only after similarities and differences across multiple real datasets have been identified.
