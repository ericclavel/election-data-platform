dataset metadata:

Dataset DOI:      doi:10.7910/DVN/PEJ5QU
Dataset ID:       3072248
Dataset version:  8.0
Release date:     2026-05-11

Target file:
  original name:  1976-2024-senate-state.csv
  file ID:        13887039
  original size:  530501 bytes
  checksum type:  MD5
  checksum:       0f8b51cf0f77a2ef0bff992f7a64d1b4


┌──────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│   column_name    │ column_type │  null   │   key   │ default │  extra  │
│     varchar      │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ year             │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ state            │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ state_po         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ state_fips       │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ state_cen        │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ state_ic         │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ office           │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ district         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ stage            │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ special          │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ candidate        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ party_detailed   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ writein          │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ mode             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ candidatevotes   │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ totalvotes       │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ unofficial       │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ version          │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ party_simplified │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


year:
DuckDB type: BIGINT
NUll count: 0
Distinct years: 26
Range: 1976 - 2024
year spans 1976–2024 and is mostly even-numbered election years, with a 2021 exception limited to Georgia runoff records.

State:
DuckDB type: VARCHAR
null count: 0
distinct states: 50
coverage: all 50 states, no D.C.

State_po:
DuckDB type: VARCHAR
null count: 0
distinct count: 50
min_length: 2
max_length: 2
format: uppercase state postal abbreviations

state_fips:
type: BIGINT
null_count: 0
distinct_count: 50
range: 1–56
mapping: exactly one state_fips value per state

state_cen:
type: DOUBLE
null_count: 0
distinct_count: 50
range: 11.0–95.0
fractional values: none
mapping: exactly one state_cen value per state

state_ic:
type: BIGINT
null_count: 0
distinct_count: 50
range: 1–82
mapping: exactly one state_ic value per state

office:
type: VARCHAR
null_count: 0
distinct_count: 1
value: US SENATE

district:
type: VARCHAR
null_count: 0
distinct_count: 1
value: statewide

stage:
type: VARCHAR
null_count: 0
distinct raw values: 5
gen: 3,616 rows
GEN: 314 rows
pre: 9 rows
runoff: 4 rows
GEN RUNOFF: 2 rows
Rare stages: pre occurs only in Georgia in 1992 and 2008; runoff only in Georgia in 2021; GEN RUNOFF only in Georgia in 2022.
stage encoding is historically inconsistent across the Senate dataset. The same conceptual election stage can be represented differently across years, and some older Georgia runoff records use gen for the runoff while pre represents the preceding general-election round.

special:
type: BOOLEAN
null_count: 0
false: 3,788 rows
true: 157 rows
special-election rows occur across 29 year/state/stage groups
special = true occurs across multiple states and years.
18 year/state/stage combinations contain both
special = false and special = true records.
special is therefore required to distinguish some
Senate election events

candidate:
type: VARCHAR
null_count: 423
distinct non-null values: 2,584

- All null candidate rows are write-in rows.
- Those null-candidate rows also have party_detailed = NULL.
- 49 write-in rows have a populated candidate value.
- Populated values are not guaranteed to represent a person
  (for example, SCATTER appears as a candidate value).

writein = true + candidate NULL
→ generic/unnamed write-in result

party_detail:

writein:

mode:

candidatevotes:

totalvotes:

unofficial:

version:

party_simplified:


*working event key- year + state + stage + special