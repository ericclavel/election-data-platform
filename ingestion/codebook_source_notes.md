check file type information for each dataverse source.

curl -sS \
  -H "X-Dataverse-key: $DATAVERSE_API_TOKEN" \
  "https://dataverse.harvard.edu/api/datasets/:persistentId/versions/:latest-published?persistentId=doi:10.7910/DVN/VOQCHQ&excludeFiles=false" \
| jq '.data.files[] | {
    label,
    id: .dataFile.id,
    originalFileName: .dataFile.originalFileName,
    contentType: .dataFile.contentType,
    size: .dataFile.filesize,
    originalSize: .dataFile.originalFileSize,
    checksum: .dataFile.checksum
}'


presidential:
-primary data
-codebook
-sources/reference file
Presidential sources reference file:
- source-provided provenance/reference artifact
- appears specific to 2020 source acquisition
- covers all 50 states plus D.C.
- records state-level election source URLs
- includes certification/status, free-text notes,
  and missing-vote indicators
- categorical values are not standardized
- does not document provenance for the full 2000–2024 series
- should be preserved raw and version-tracked independently

house:
-primary data
-codebook
House codebook:
- current coverage matches the 1976–2024 dataset
- substantially more current than the Senate codebook
- documents at-large district coding and fusion-ticket behavior
- documents uncontested-race handling using candidatevotes = 1
- does not document observed -1 sentinel values
- contains some internal casing inconsistencies
- generally useful, but still requires empirical validation against the data

senate:
-primary data
-codebook
-sources/reference file

primary data
    1976-2024-senate-state.csv

codebook
    codebook-us-senate-1976–2024.md
    → actually contains older 1976–2018 documentation

provenance/reference
    sources-senate.csv
    → source tracking for a particular acquisition period,
      apparently centered on 2020
Senate sources reference file:
- source-provided provenance/reference artifact
- appears focused on 2020 Senate result acquisition
- records state-level source URLs, certification/status notes,
  free-text data-quality notes, and missing-vote indicators
- categorical values are not standardized
- should be preserved raw and version-tracked independently


DatasetConfig
│
├── primary data config
│
└── reference_assets
    ├── codebook
    │   └── explicit discovery rule
    │
    └── sources
        └── explicit discovery rule

curl -sS -L \
  -H "X-Dataverse-key: $DATAVERSE_API_TOKEN" \
  "https://dataverse.harvard.edu/api/access/datafile/4304792"


Ssynchronization system needs to distinguish between source metadata changed from source artifact content changed.