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

party_detailed:
- type: VARCHAR
- null_count: 627
- distinct non-null values: 195
- contains major parties, minor parties, historical parties,
  affiliation-status labels, combined/fusion labels, and reporting labels
- contains semantically similar but differently encoded values
  (for example DEMOCRAT vs DEMOCRATIC)
- should be preserved as raw source data rather than normalized during ingestion

writein:
- type: BOOLEAN
- false: 3,473 rows
- true: 472 rows
- no apparent NULL values
- of the 472 write-in rows:
  - 423 have candidate = NULL
  - 49 have a populated candidate value
- writein = true therefore includes both unnamed/generic write-in totals
  and specifically named write-in candidates

mode:
type: VARCHAR
distinct raw values: 2

total:
- 3,629 rows
- 1976–2021

TOTAL:
- 316 rows
- 2022–2024


candidatevotes:
type: DOUBLE
null_count: 0
range: 1–9,036,252
fractional values: 0


totalvotes:
- type: DOUBLE
- null_count: 0
- range: 1–15,348,846
- fractional values: 0


unofficial:
- type: BOOLEAN
- false: 3,924 rows
- true: 21 rows
- true values occur across 9 year/state/stage/special groups
- unofficial is a meaningful source flag, not a constant


version:
- type: VARCHAR
- null_count: 0
- 4 distinct raw values
- appears to represent source revision/update metadata
- formatting is inconsistent (YYYYMMDD and MM/DD/YY)
- version can differ within the same election year
- in 2024, regular contests use 11/20/25 while the California and
  Nebraska special-election records use 20241212
- preserve as raw metadata rather than interpreting it as a numeric field

party_simplified:
- type: VARCHAR
- values: OTHER, DEMOCRAT, REPUBLICAN, LIBERTARIAN, NULL
- only 2 NULL rows
- both NULL rows are non-party reporting categories
- source-provided broad classification should be preserved separately
  from party_detailed


*working event grain:
- identified by year + state + stage + special
- 862 event groups
- totalvotes is consistent within every event group
- no groups contain multiple distinct totalvotes values
- Generally groups Senate election events correctly, but is not universally unique.
At least one known exception is Louisiana 2002, where multiple election rounds
share the same event descriptors.
-Row-level findings:
- 3,945 total rows
- no exact duplicate rows
- every raw row is distinct across the full set of columns
- descriptive fields alone are not always sufficient to uniquely identify a row
- unnamed write-in rows can collide on candidate/party/writein/mode
- Louisiana 2002 is the only observed named-candidate case where
  multiple election rounds are not distinguishable by the event fields

  year
+ state
+ stage
+ special
+ candidate
+ party_detailed
+ writein
+ mode
+ candidatevotes
  -These fields do form a unique row identifier.
  - The raw rows are unique.
- A descriptive natural key without candidatevotes is not always available.
- Adding candidatevotes makes the rows unique.
- candidatevotes should still be treated as a measure, not as a true identity field.


Data quality finding: 2002 Louisiana contains multiple election rounds that cannot be
distinguished from the available stage/special fields.

Mary Landrieu and Suzanne Haik Terrell each appear twice with different
candidate vote totals corresponding to the November 5 election and
December 7 runoff.

Both rounds are encoded stage='gen', special=false, and mode='total'.

The source therefore does not provide enough fields to construct a
universally unique election-event key from year + state + stage + special.

Unnamed write-in rows:
- candidate = NULL
- party_detailed = NULL
- writein = true
- multiple such rows can occur within the same election event
- within every observed repeated group, each row has a distinct candidatevotes value
- therefore the rows are distinct in the source, but cannot be uniquely
  identified using descriptive candidate/party fields alone


Vote integrity:
- candidatevotes never exceeds totalvotes
- within every year + state + stage + special group,
  SUM(candidatevotes) = totalvotes
- vote totals are internally consistent
- arithmetic consistency does not guarantee that the event key
  represents exactly one real-world election round