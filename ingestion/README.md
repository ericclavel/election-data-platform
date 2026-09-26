# Ingestion

## Purpose

The ingestion subsystem retrieves primary source data and source-provided reference assets such as codebooks and provenance files.

It is responsible for:

* Querying upstream metadata
* Locating configured source and reference files
* Detecting upstream changes
* Downloading original files when required
* Validating file size and upstream checksums
* Calculating local SHA-256 fingerprints
* Preserving validated files without transformation
* Recording current upstream and local file state

Ingestion is intentionally separated from downstream schema normalization, cleaning, transformation, and analytical modeling.

## Configuration

Dataset and reference-asset configuration is defined in:

```text
ingestion/config.py
```

Each dataset is represented by a `DatasetConfig`:

```text
source
dataset
dataset_doi
file_prefix
reference_assets
```

Optional source-provided reference files are represented by `ReferenceAsset`:

```text
name
match_field
file_prefix
```

`match_field` identifies which upstream metadata field is used to locate the asset, such as Dataverse `label` or `originalFileName`.

Configured datasets are collected in `DATASETS`.

`DatasetConfig` also derives storage paths for:

```text
raw_data_dir
data_metadata_path
reference_data_dir
reference_metadata_path(asset_name)
```

This keeps source-specific identifiers and storage conventions centralized rather than duplicated across ingestion scripts.

## Execution

Primary-data ingestion:

```bash
docker compose up --build ingestion
```

Reference-asset synchronization:

```bash
docker compose up --build reference-sync
```

Both services use the same project image, dependencies, credentials, and bind-mounted `data/` directory while running separate ingestion workflows.

Environment variables are supplied through the project `.env` file.

The containers run using the host development user's UID and GID so bind-mounted files remain writable by the host user.

## Workflow

Both scripts follow the same general orchestration pattern:

```text
main()
  ↓
configure logging
  ↓
validate configuration
  ↓
iterate through DATASETS
  ↓
run script-specific workflow
```

Primary data is processed by:

```text
ingest_dataset(config)
```

Reference assets are processed by:

```text
sync_reference_assets(config)
  ↓
iterate through config.reference_assets
```

The shared high-level acquisition flow is:

```text
query upstream metadata
        ↓
locate configured file
        ↓
load locally recorded state
        ↓
compare remote and local state
        ↓
determine required action
        ↓
download when required
        ↓
validate size and upstream checksum
        ↓
calculate local SHA-256
        ↓
persist validated file
        ↓
update local metadata
```

Each dataset and reference asset is evaluated independently so unchanged items can be skipped without preventing remaining items from being checked.

## Change Detection

Primary-data ingestion treats changes to the configured source state as requiring ingestion.

Compared fields include:

* Dataset version
* File ID
* File name
* Upstream checksum type
* Upstream checksum

Reference assets are synchronized more granularly because upstream metadata can change without the underlying file contents changing:

```text
content checksum changed
→ download, validate, and update metadata

remote metadata changed only
→ update metadata without downloading again

no change
→ skip
```

This allows fields such as dataset version, file ID, and Dataverse label to evolve independently from the reference file contents.

## Validation and Safe Downloads

Downloaded files must:

* Exist as regular files
* Be non-empty
* Match the upstream file size when available
* Match the upstream checksum

Current Dataverse files use MD5 as the upstream checksum.

After upstream validation succeeds, the ingestion process records a local SHA-256 fingerprint.

Downloads are first written to a temporary `.part` file and moved to their final destination only after the download completes successfully. Failed partial downloads are removed.

Local ingestion state is not advanced when required download or validation steps fail.

## Storage and Metadata

Primary source files:

```text
data/raw/<source>/<dataset>/<dataset_version>/
```

Reference assets:

```text
data/reference/<source>/<dataset>/<dataset_version>/
```

Files are preserved in their original source format rather than converted for downstream convenience.

Primary-data metadata:

```text
data/metadata/<source>/<dataset>/data.json
```

Reference-asset metadata:

```text
data/metadata/<source>/<dataset>/reference/<asset_name>.json
```

Metadata may include:

```text
dataset DOI
dataset version
file ID
file name
Dataverse label
original file name
file size
upstream checksum
local SHA-256 fingerprint
retrieval timestamp
```

Separating metadata by asset allows primary data, codebooks, and provenance files to evolve independently.

## Failure Behavior

Ingestion fails rather than advancing local state when required operations do not complete successfully.

Failures may include:

* Upstream or network errors
* Authorization failures
* Missing expected files
* Filesystem write errors
* File-size mismatches
* Checksum mismatches
* Invalid or incomplete source metadata

This ensures that recorded local file state represents validated source content.

## Environment

Dataverse credentials are supplied through:

```text
.env
```

using:

```text
DATAVERSE_API_TOKEN=<your-token>
```

The `.env` file is excluded from Git and the Docker build context and is injected into the ingestion services at runtime.

Required variables are documented in `.env.example`.

## Source Documentation

Dataset-specific documentation is stored under:

```text
docs/sources/<source>/<dataset>/
```

Each dataset currently contains:

```text
README.md
source_schema.md
data_quality_findings.md
```

Documentation responsibilities are intentionally separated:

```text
ingestion/README.md
→ shared ingestion architecture and behavior

dataset README.md
→ source identity, coverage, source-specific metadata, and available reference assets

source_schema.md
→ observed source schema and field behavior

data_quality_findings.md
→ source-specific anomalies and empirical findings
```

Shared behavior such as Docker execution, storage conventions, synchronization logic, checksum validation, metadata layout, and reference-asset handling is documented here rather than repeated in individual dataset READMEs.

Datasets compatible with the existing Dataverse workflow are added by defining a `DatasetConfig`, configuring any associated `ReferenceAsset` entries, and adding the dataset to `DATASETS`.

Source interpretation and normalization remain outside the ingestion layer.

New ingestion abstractions should be introduced only when differences observed across real sources justify them.
