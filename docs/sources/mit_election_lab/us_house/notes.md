Dataverse filename: 1976-2024-house.tab
Actual downloaded content: comma-delimited

Shared with presidential:
year
state
state_po
office
candidate
party
mode
candidatevotes
totalvotes
version

House specific:
state_fips
state_cen
state_ic
district
stage
runoff
special
writein
unofficial
fusion_ticket


runoff → VARCHAR in raw inspection.  Values True, False, NA

year
state
state_po
state_fips
state_cen
state_ic
office
district
stage
runoff
special
candidate
party
writein
mode
candidatevotes
totalvotes
unofficial
version
fusion_ticket




year:
- DuckDB type: BIGINT
- Null count: 0
- Distinct values: 25
- Range: 1976–2024
- Observed values follow a two-year election cadence


state
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 51
- Includes the 50 states plus District of Columbia
- Values are consistently uppercase

state_po
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 51
- Two-character uppercase postal abbreviations
- Includes the 50 states plus DC

state_fips
- DuckDB type: BIGINT
- Null count: 0
- Distinct values: 51
- One value per state/DC
- Values are consistent with state FIPS codes
- Semantically an identifier rather than a numeric measure
- Likely downstream type: VARCHAR

state_cen
- DuckDB type: BIGINT
- Null count: 0
- Distinct values: 51
- One value per state/DC
- Appears to be a Census state identifier
- Semantically an identifier rather than a numeric measure
- Exact field definition should be confirmed against the source codebook

state_ic
- DuckDB type: BIGINT
- Null count: 0
- Distinct values: 51
- One value per state/DC
- Appears to be a state identifier/coding scheme
- Semantically an identifier rather than a numeric measure
- Exact field definition should be confirmed against the source codebook

office
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 1
- Observed value: US HOUSE
- Constant across the dataset

district
- DuckDB type: BIGINT
- Null count: 0
- Distinct values: 54
- Observed range: 0–53
- `0` is used for statewide / at-large reporting
- District numbering changes historically as congressional apportionment changes
- Semantically a geographic identifier rather than a numeric measure

stage
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 2
- GEN: 33,745 rows
- PRI: 60 rows
- Appears to distinguish general and primary election records

runoff
- Raw inspection type: VARCHAR
- SQL null count: 0
- Distinct raw values: TRUE, FALSE, NA
- FALSE: 25,141
- NA: 8,656
- TRUE: 8
- `NA` is a literal source value, not SQL NULL
- `NA` is concentrated in GEN rows from 2006–2018
- TRUE appears in four district-year contests
- DuckDB BOOLEAN auto-inference is unsafe for this column
- Exact semantic meaning of `NA` still needs codebook confirmation

special
- DuckDB type: BOOLEAN
- Null count: 0
- Distinct values: false, true
- false: 33,715 rows
- true: 90 rows
- Clean boolean field

candidate
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 16,975
- Contains person names plus non-person reporting categories
- Examples include WRITEIN, OTHER, BLANK VOTE, SCATTERING, VOID, UNDERVOTES
- Should not be treated as a clean candidate dimension without downstream classification/normalization

party
- DuckDB type: VARCHAR
- Null count: 0
- Distinct raw values: 500
- Literal `NA` is a source value, not SQL NULL
- Contains major parties, minor parties, local/historical labels, affiliation-status labels, write-in labels, and spelling variation
- Raw source vocabulary should be preserved before any downstream normalization

writein
- DuckDB type: BOOLEAN
- Null count: 0
- Distinct values: 2
- false: 30,956
- true: 2,849
- Clean boolean field

mode
- DuckDB type: VARCHAR
- Null count: 0
- Distinct values: 1
- Observed value: TOTAL
- Constant across all 33,805 rows

candidatevotes
- DuckDB type: BIGINT
- SQL null count: 0
- Minimum: -1
- Maximum: 387,109
- `-1` occurs in exactly one row
- `-1` should be treated as a source sentinel, not a literal negative vote count
- Exact sentinel semantics should still be confirmed against the MEDSL codebook

totalvotes
- DuckDB type: BIGINT
- SQL null count: 0
- Minimum: -1
- Maximum: 656,104
- `-1` occurs in 3 rows
- Observed negative values appear to be sentinel values rather than literal vote totals
- Sentinel behavior differs somewhat from `candidatevotes`
- Exact source convention still needs codebook confirmation

unofficial
- DuckDB type: BOOLEAN
- SQL null count: 0
- Distinct values: false, true
- false: 33,766
- true: 39
- TRUE appears only in 2018
- TRUE rows are limited to North Carolina and West Virginia
- Exact source definition should still be confirmed from the codebook

version
- DuckDB type: BIGINT
- SQL null count: 0
- Distinct values: 1
- Observed value: 20250910
- Constant across all 33,805 rows
- Looks like a YYYYMMDD-style version stamp
- Semantically metadata, not a numeric measure

fusion_ticket
- DuckDB type: BOOLEAN
- SQL null count: 0
- Distinct values: false, true
- false: 31,128 rows
- true: 2,677 rows
- Clean boolean field syntactically
- Exact MEDSL definition should still be confirmed from the codebook



A row represents a reported candidate/result line within a House election event, but the available descriptive fields do not always uniquely identify that reporting line.

- 0 exact duplicates across all 20 source columns
- Every physical row in the file is unique

The descriptive-key ambiguity is isolated to write-in records.
For all writein = FALSE rows, this combination is unique:
    year
    state
    district
    stage
    runoff
    special
    candidate
    party
    writein
    mode

    One row represents one candidate-party result line within a particular House election event.

- Multi-party candidate rows: strongly associated with fusion/cross-endorsement,
  especially New York, but not exclusively New York.

- fusion_ticket inconsistency:
  observed only for 2024 New York in our current test.


Grain: One row represents one candidate-party result line within a specific House election event.

With one documented exception/qualification:

Generic WRITEIN result lines can repeat with identical descriptive fields and differ only by candidatevotes, so the available descriptive fields do not form a universally reliable natural key.

Data quality finding: totalvotes is not guaranteed to be constant across every row belonging to the same election event.
    -For these five 2018 Georgia contests, named-candidate rows carry a totalvotes value excluding write-ins, while the WRITEIN row carries a totalvotes value including the write-in votes.



    2018 Maine CD-2 contains internally inconsistent ranked-choice values: candidate vote totals correspond to an earlier tabulation, while totalvotes corresponds to the later final tabulation.
        candidatevotes → earlier 11/15 tabulation
        totalvotes     → later final 11/21 continuing-ballot total