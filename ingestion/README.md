# Ingestion

## Purpose

The ingestion subsystem is responsible for retrieving raw source data, validating downloaded files, preserving source data without transformation, and recording the most recently validated source state.

Ingestion is intentionally separated from downstream schema normalization, cleaning, transformation, and analytical modeling.

## Responsibilities

The ingestion layer is responsible for:

* Querying upstream source metadata
* Identifying the current published source version
* Locating the expected source file
* Detecting whether the upstream source has changed
* Requesting authorized source-file access when required
* Downloading the original source file
* Validating file size
* Verifying the upstream checksum
* Calculating a local SHA-256 fingerprint
* Persisting validated raw files
* Updating local ingestion metadata only after successful validation

The ingestion layer does not modify or normalize raw source values.

## Execution

The ingestion service is run through Docker Compose from the project root:

```bash
docker compose up --build ingestion
```

Docker provides the Python environment, dependencies, and ingestion code.

Environment variables are supplied to the container at runtime through the project's `.env` file.

## Ingestion Workflow

```text
Configured source
      ↓
Query current published source metadata
      ↓
Locate target source file
      ↓
Load locally recorded source metadata
      ↓
Compare remote and local source state
      ↓
Source unchanged?
├── Yes → Exit successfully
└── No
     ↓
Request source-file access
     ↓
Download original source file
     ↓
Validate downloaded file
     ↓
Verify upstream checksum
     ↓
Calculate local SHA-256 fingerprint
     ↓
Persist validated raw source
     ↓
Update local ingestion metadata
```

## Source Change Detection

Each source maintains local metadata describing the most recently validated upstream source.

The ingestion process compares the current upstream metadata against the locally recorded state.

Relevant comparison fields currently include:

* Dataset version
* File ID
* File name
* Upstream checksum type
* Upstream checksum value

If no relevant source metadata has changed, ingestion exits without downloading the file again.

Example:

```text
INFO | Source has not changed. No ingestion needed.
```

If a change is detected, ingestion proceeds with download and validation.

Example:

```text
INFO | Change detected: dataset_version (20.0 -> 21.0)
INFO | Source has changed. Proceeding with ingestion.
```

## Download Validation

Downloaded files are validated before local ingestion metadata is updated.

### File Validation

The downloaded source file must:

* Exist
* Be a regular file
* Be non-empty
* Match the original file size reported by the upstream source when available

Example:

```text
INFO | Validating downloaded file...
INFO | Downloaded file validation passed.
```

### Upstream Checksum Validation

The local download is verified against the checksum reported by the upstream source.

For the current Dataverse sources, this is an MD5 checksum associated with the original source file.

Example:

```text
INFO | Validating Dataverse checksum...
INFO | Dataverse checksum validation passed.
```

### Local Fingerprint

After upstream validation succeeds, the ingestion process calculates a local SHA-256 fingerprint.

The upstream checksum and local fingerprint serve different purposes:

* Upstream checksum — verifies that the downloaded file matches the source-provided file
* Local SHA-256 — provides a strong local fingerprint for the persisted raw file

## Safe Downloads

Downloads are written to a temporary `.part` file before being moved to their final destination.

Conceptually:

```text
source_file.csv.part
        ↓
download completes
        ↓
validation succeeds
        ↓
source_file.csv
```

If the download fails, the partial file is removed and the final destination is not replaced.

This prevents incomplete downloads from appearing as successfully ingested source files.

## Metadata Updates

Local ingestion metadata is stored under:

```text
data/metadata/<source>/<dataset>/current.json
```

The metadata record represents the most recent upstream source that was successfully downloaded and validated locally.

A typical metadata record contains information such as:

```text
dataset DOI
dataset version
file ID
file name
upstream checksum type
upstream checksum
local SHA-256 fingerprint
retrieval timestamp
```

`current.json` must not be updated if download or validation fails.

## Raw Data Storage

Validated source files are stored under:

```text
data/raw/<source>/<dataset>/<dataset_version>/
```

Raw files are preserved in their original source format.

Examples may include:

```text
.csv
.tab
.tsv
```

The ingestion layer should not convert source formats simply to make downstream processing more convenient.

## Expected Logging

### No Source Change

A normal no-op ingestion run should resemble:

```text
INFO | Source has not changed. No ingestion needed.
```

This indicates that the upstream source was checked successfully and matches the locally recorded state.

### Source Change Detected

A successful update path may resemble:

```text
INFO | Change detected: dataset_version (20.0 -> 21.0)
INFO | Source has changed. Proceeding with ingestion.
INFO | Validating downloaded file...
INFO | Downloaded file validation passed.
INFO | Validating Dataverse checksum...
INFO | Dataverse checksum validation passed.
```

Additional logging may be added as ingestion expands to multiple sources.

## Failure Behavior

The ingestion process is designed to fail before advancing local source state when required validation does not succeed.

Failures may include:

* Upstream HTTP errors
* Network connection failures
* Authorization failures
* Missing expected source files
* Filesystem write failures
* File-size mismatches
* Checksum mismatches
* Invalid or incomplete source metadata

A failed ingestion must not update `current.json`.

This ensures that locally recorded ingestion state always represents a source file that completed the required validation process.

## Environment Configuration

Required credentials are supplied through the project `.env` file.

For Dataverse ingestion:

```text
DATAVERSE_API_TOKEN=<your-token>
```

The `.env` file:

* Is not committed to Git
* Is excluded from the Docker build context
* Is injected into the ingestion container at runtime

Required environment variables are documented in the root `.env.example`.

## Source-Specific Documentation

Dataset-specific source behavior is documented separately under:

```text
docs/sources/<source>/<dataset>/
```

Each dataset directory contains:

```text
README.md
source_schema.md
data_quality_findings.md
```

The ingestion README documents shared ingestion behavior rather than duplicating source-specific metadata.

## Adding New Sources

As new datasets are introduced, the ingestion architecture should favor reuse of shared behavior rather than creating independent implementations for each source.

Source-specific configuration may include:

* Dataset identifier or DOI
* Source-file selector
* Raw-data destination
* Metadata destination
* Authentication requirements
* Source-specific access behavior

Shared behavior such as metadata comparison, downloading, validation, checksum verification, fingerprinting, and state updates should remain reusable wherever possible.

The exact multi-source ingestion design will be generalized after multiple real datasets have been inspected and their differences are understood.
