# U.S. House 1976–2024

## Overview

This dataset contains district-level election returns for U.S. House of Representatives elections from 1976 through 2024.

It provides the platform with historical congressional election results at the congressional-district level and introduces source characteristics that differ from the county presidential dataset, including district identifiers, election-stage fields, special-election and runoff indicators, write-in records, and fusion-ticket reporting.

Detailed field behavior and source-specific data-quality findings are documented separately.

## Source

* Source organization: `MIT Election Data and Science Lab (MEDSL)`
* Source system: `Harvard Dataverse`
* Dataset name: `U.S. House 1976–2024`
* DOI / persistent ID: `doi:10.7910/DVN/IG0UN2`
* Dataset ID: `3059095`
* Access method: `Harvard Dataverse API with original-file download via signed URL`
* Authentication requirements: `Dataverse API token required for the tested download workflow`
* Guestbook requirements: `General guestbook (ID 458)`

## Current Source Metadata

* Current published dataset version: `15.0`
* Version ID: `721192`
* Release time: `2026-03-09T17:49:25Z`
* Target source file: `1976-2024-house.tab`
* File ID: `13592823`
* File format: `Dataverse identifies the file as TSV; the downloaded original content is comma-delimited`
* Original file size: `4,156,562 bytes`
* Dataverse file size: `4,229,898 bytes`
* Checksum type: `MD5`
* Checksum value: `a9566ac393913a1af343284e837c17bb`

## Coverage

* Offices: `U.S. House of Representatives`
* Election Years: `1976–2024, every two years (25 election years)`
* Geography: `Congressional district / constituency`
* Time range: `1976–2024`
* Grain: `One candidate-party result line within a specific House election event, with source-specific exceptions for generic write-in reporting`

The observed election-event fields are:

```text
year
state
district
stage
runoff
special
```

Generic `WRITEIN` rows can repeat with identical descriptive fields and different vote totals, so the source does not provide a universally reliable descriptive natural key for every physical row.

## Local Storage

### Raw Data

```text
data/raw/mit_election_lab/us_house/15.0/1976-2024-house.tab
```

Raw source files should be preserved without modification and stored under the source dataset version.

### Ingestion Metadata

Expected metadata location when this source is integrated into the ingestion workflow:

```text
data/metadata/mit_election_lab/us_house/current.json
```

The metadata record should preserve enough information to reproduce and validate ingestion, including at minimum:

* dataset version
* file ID
* source file name
* Dataverse checksum type and value
* local checksum
* retrieval timestamp

## Related Documentation

* [Source Schema](./source_schema.md)
* [Data Quality Findings](./data_quality_findings.md)

## Ingestion Notes

The House source has been downloaded and inspected locally but has not yet been generalized into the reusable ingestion workflow.

Several source characteristics are important for future ingestion:

* The source file is named `1976-2024-house.tab` and Dataverse identifies it as tab-separated, but the downloaded original content is comma-delimited.
* File parsing should therefore inspect or auto-detect the physical delimiter rather than infer it solely from the file extension or Dataverse format label.
* The `runoff` column cannot safely rely on automatic Boolean inference because the raw field contains `TRUE`, `FALSE`, and literal `NA`.
* Literal source values such as `NA` must remain distinguishable from SQL `NULL`.
* Vote fields contain source sentinel values such as `-1`; raw ingestion should preserve these values rather than assigning downstream semantics during download.
* Candidate and party values should be preserved exactly as provided by the source before any normalization.
* Raw files should remain versioned and immutable so future source releases can be compared with the currently ingested version.

The manual source-acquisition workflow used during inspection demonstrated that the Dataverse endpoint can provide a temporary signed URL for downloading the original file. Signed URLs are temporary and should be requested immediately before download rather than stored for reuse.



## Reference Assets

The source provides:

* Dataset codebook

Reference assets are synchronized and versioned by the shared ingestion
workflow documented in `ingestion/README.md`.