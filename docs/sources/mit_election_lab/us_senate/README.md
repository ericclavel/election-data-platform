# U.S. Senate Statewide 1976–2024

## Overview

This dataset contains statewide U.S. Senate election results from 1976 through 2024.

It provides candidate/result-level vote totals, party information, write-in indicators, special-election flags, election-stage information, and source metadata.

Within the election data platform, this dataset provides the historical Senate-results source and helps establish how statewide congressional election data differs from the existing presidential and U.S. House sources.

## Source

* Source organization: `MIT Election Data and Science Lab (MEDSL)`
* Source system: `Harvard Dataverse`
* Dataset name: `U.S. Senate statewide 1976–2024`
* DOI / persistent ID: `doi:10.7910/DVN/PEJ5QU`
* Access method: `Harvard Dataverse API / signed original-file download`
* Authentication requirements: `Required for the signed file-download workflow used by ingestion`
* Guestbook requirements: `Required; Harvard Dataverse General guestbook (ID 458)`

## Current Source Metadata

* Current published dataset version: `8.0`
* Release time: `2026-05-11T16:13:52Z`
* Target source file: `1976-2024-senate-state.csv`
* File ID: `13887039`
* File format: `CSV`
* Original file size: `530501 bytes`
* Checksum type: `MD5`
* Checksum value: `0f8b51cf0f77a2ef0bff992f7a64d1b4`

The Dataverse file listing exposes the data file with a `.tab` label, while the original-format download is the CSV file `1976-2024-senate-state.csv`. The ingestion workflow requests the original file format.

## Coverage

* Offices: `U.S. Senate`
* Election years: `1976–2024; primarily even-numbered election years, with 2021 Georgia runoff records also present`
* Geography: `Statewide; all 50 states, no District of Columbia`
* Time range: `1976–2024`
* Grain: `One reported candidate/result line within a Senate election event as represented by the source`

The working event grouping is:

```text
year + state + stage + special
```

This grouping generally identifies Senate election events but is not universally unique. Known edge cases are documented in `data_quality_findings.md`.

## Local Storage

### Raw Data

```text
data/raw/mit_election_lab/us_senate/<dataset_version>/<source_file>
```

Current version:

```text
data/raw/mit_election_lab/us_senate/8.0/1976-2024-senate-state.csv
```

### Ingestion Metadata

```text
data/metadata/mit_election_lab/us_senate/current.json
```

The metadata record tracks the currently ingested source version and file, including:

* dataset DOI
* dataset version
* Dataverse file ID
* source file name
* Dataverse checksum
* locally computed SHA256 checksum
* retrieval timestamp

## Related Documentation

* [`source_schema.md`](source_schema.md) — source columns, inferred types, categorical values, identifiers, nullability, and observed grain
* [`data_quality_findings.md`](data_quality_findings.md) — source inconsistencies, repeated-row behavior, election-stage issues, vote-field checks, and known edge cases

## Ingestion Notes

The Senate dataset uses the shared configuration-driven Harvard Dataverse ingestion workflow.

Its dataset configuration supplies:

```text
source: mit_election_lab
dataset: us_senate
dataset DOI: doi:10.7910/DVN/PEJ5QU
target file prefix: 1976-2024-senate-state
```

The ingestion process:

1. Requests the latest published dataset metadata from Harvard Dataverse.
2. Identifies the configured target source file.
3. Compares the remote source metadata with the local `current.json`.
4. Skips ingestion when the recorded source has not changed.
5. Requests an authenticated guestbook-aware signed download URL when a change is detected.
6. Downloads the original source file to the versioned raw-data directory.
7. Validates the downloaded file and Dataverse MD5 checksum.
8. Computes a local SHA256 checksum.
9. Updates `current.json` only after successful validation.

Raw source values are preserved during ingestion. Source-specific interpretation and normalization are intentionally deferred to later staging/modeling work.



## Reference Assets

The source provides:

* Dataset codebook
* Source-provenance file

Reference assets are synchronized and versioned by the shared ingestion
workflow documented in `ingestion/README.md`.