# County Presidential Election Returns

## Overview

This dataset contains county-level U.S. presidential election returns from 2000 through 2024. It serves as the initial election-results source for the platform and provides historical candidate and vote totals at the county level.

## Source

* Source organization: `MIT Election Data and Science Lab`
* Source system: `Harvard Dataverse`
* Dataset name: `County Presidential Election Returns 2000–2024`
* DOI / persistent ID: `doi:10.7910/DVN/VOQCHQ`
* Dataverse dataset ID: `3239428`
* Access method: `Harvard Dataverse API`
* Authentication requirements: `Dataverse API token required for source-file download`
* Guestbook requirements: `Guestbook ID 458 requires Name, Email, Institution, and Position`

## Current Source Metadata

* Current published dataset version: `20.0`
* Release time: `2026-02-25T19:00:32Z`
* Target source file: `countypres_2000-2024.csv`
* File ID: `13573089`
* File format: `CSV`
* Original file size: `10,222,208 bytes`
* Checksum type: `MD5`
* Checksum value: `bd6661282936006b4ef4f5ee71418f3e`

## Coverage

* Office: `U.S. President`
* Geography: `County`
* Time range: `2000–2024`
* Election years: `2000, 2004, 2008, 2012, 2016, 2020, 2024`
* Grain: `One row per reported candidate/party/mode combination within a county and election year`

## Local Storage

### Raw Data

```text
data/raw/mit_election_lab/county_presidential/
```

Raw source files are stored by Dataverse dataset version:

```text
data/raw/mit_election_lab/county_presidential/
└── <dataset_version>/
    └── <source_file>
```

For the current source:

```text
data/raw/mit_election_lab/county_presidential/
└── 20.0/
    └── countypres_2000-2024.csv
```

### Ingestion Metadata

```text
data/metadata/mit_election_lab/county_presidential/current.json
```

`current.json` records the most recent source version that was successfully downloaded and validated locally.

## Related Documentation

* [Source Schema](./source_schema.md)
* [Data Quality Findings](./data_quality_findings.md)

## Ingestion Notes

The source file is retrieved through the Harvard Dataverse API using the original-file format.

Before the local ingestion metadata is updated, the pipeline validates the downloaded file against the original file size and MD5 checksum reported by Dataverse. A local SHA-256 fingerprint is then calculated and recorded in `current.json`.

Raw source data is preserved without transformation. Schema normalization, type casting, cleaning, and analytical modeling occur downstream.
