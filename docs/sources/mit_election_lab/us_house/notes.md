Dataverse filename: 1976-2024-house.tab
Actual downloaded content: comma-delimited


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



    Generic WRITEIN normalization can cause SUM(candidatevotes) to understate totalvotes, because multiple distinct write-in candidates may be collapsed or omitted in the standardized rows.



Election event:
year + state + district + stage + runoff + special

Result-line grain:
election event + candidate + party + writein + mode



2024 New York → BLANK / VOID excluded from totalvotes
2024 Maine 1 → BLANK excluded
2002 Indiana + 2012/2016 Connecticut → lossy generic write-in representation
2018 Maine 2 → ranked-choice tabulation inconsistency
2024 Florida 20 / Oklahoma 3 → -1 sentinel/unopposed cases





# U.S. House 1976–2024 — Source Schema

## Source File

* Dataset: U.S. House 1976–2024
* Source organization: MIT Election Data and Science Lab (MEDSL)
* Source file: `1976-2024-house.tab`
* Dataset version inspected: `15.0`
* Rows: `33,805`
* Columns: `20`
* File extension / advertised format: `.tab` / tab-separated
* Observed delimiter: comma-separated

Despite the `.tab` file extension and Dataverse format metadata, the downloaded original source file is comma-delimited. DuckDB correctly detects the delimiter when using `read_csv_auto()` without an explicit tab delimiter.

## Columns

| Column           | Source Type              | DuckDB Type                     | Description                                                              | Notes                                                                                                              |
| ---------------- | ------------------------ | ------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `year`           | Integer                  | `BIGINT`                        | Election year                                                            | 25 distinct even-numbered election years from 1976–2024                                                            |
| `state`          | Text                     | `VARCHAR`                       | State name                                                               | 51 values: 50 states + District of Columbia                                                                        |
| `state_po`       | Text                     | `VARCHAR`                       | U.S. postal abbreviation                                                 | 51 distinct values                                                                                                 |
| `state_fips`     | Identifier               | `BIGINT`                        | State FIPS code                                                          | Numeric in source but semantically an identifier                                                                   |
| `state_cen`      | Identifier               | `BIGINT`                        | U.S. Census state code                                                   | Numeric in source but semantically an identifier                                                                   |
| `state_ic`       | Identifier               | `BIGINT`                        | ICPSR state code                                                         | Numeric in source but semantically an identifier                                                                   |
| `office`         | Text                     | `VARCHAR`                       | Office being contested                                                   | Constant value: `US HOUSE`                                                                                         |
| `district`       | Identifier               | `BIGINT`                        | Congressional district number                                            | Values 0–53; `0` represents at-large/statewide districts                                                           |
| `stage`          | Categorical              | `VARCHAR`                       | Election stage                                                           | Observed values: `GEN`, `PRI`                                                                                      |
| `runoff`         | Boolean-like categorical | Auto-inferred `BOOLEAN`; unsafe | Indicates runoff status                                                  | Raw values are `TRUE`, `FALSE`, and literal `NA`; should be read as `VARCHAR` during raw inspection                |
| `special`        | Boolean                  | `BOOLEAN`                       | Indicates special-election status                                        | Clean Boolean field                                                                                                |
| `candidate`      | Text                     | `VARCHAR`                       | Candidate or source reporting label                                      | Includes person names and non-person categories such as `WRITEIN`, `BLANK`, `VOID`, `SCATTERING`, and `UNDERVOTES` |
| `party`          | Text                     | `VARCHAR`                       | Party associated with the result line                                    | 500 distinct raw labels; includes literal `NA`, minor parties, local labels, and spelling variation                |
| `writein`        | Boolean                  | `BOOLEAN`                       | Indicates write-in result lines                                          | Clean Boolean field                                                                                                |
| `mode`           | Categorical              | `VARCHAR`                       | Voting/reporting mode                                                    | Constant value `TOTAL` in the inspected file                                                                       |
| `candidatevotes` | Integer measure          | `BIGINT`                        | Votes associated with the candidate-party result line                    | Contains a `-1` sentinel in one observed row                                                                       |
| `totalvotes`     | Integer measure          | `BIGINT`                        | Reported total votes for the election event                              | Contains `-1` sentinel values and is not always constant across all rows in an event                               |
| `unofficial`     | Boolean                  | `BOOLEAN`                       | Indicates unofficial results                                             | `TRUE` occurs only in 2018 North Carolina and West Virginia in the inspected file                                  |
| `version`        | Date-like metadata       | `BIGINT`                        | Dataset finalization/version stamp                                       | Constant `20250910`; semantically date/version metadata rather than a numeric measure                              |
| `fusion_ticket`  | Boolean                  | `BOOLEAN`                       | Identifies party lines associated with fusion/cross-endorsed candidacies | Candidates may appear multiple times under different party labels                                                  |

## Key Fields

### Election Event

The following combination is the current working identifier for a House election event:

```text
year
state
district
stage
runoff
special
```

Inspection did not identify evidence requiring an additional event-level field.

Differences in `totalvotes` within some event groups were traced to source/reporting conventions rather than separate election events.

### Result-Line Grain

For ordinary non-write-in records, the following descriptive combination was unique in the inspected source:

```text
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
```

A practical description of the observed row grain is:

> One row represents one candidate-party result line within a specific U.S. House election event.

This description requires an important qualification: generic `WRITEIN` rows can repeat with the same descriptive fields while carrying different `candidatevotes`.

Therefore, the available descriptive fields do not form a universally reliable natural key.

### Exact Duplicate Check

No exact duplicate rows were found when comparing all 20 source columns.

## Identifier Handling

### State Identifiers

The source contains multiple state coding systems:

* `state`
* `state_po`
* `state_fips`
* `state_cen`
* `state_ic`

Each maps cleanly to the same 51 state/DC entities in the inspected data.

Although `state_fips`, `state_cen`, and `state_ic` are stored numerically, they are identifiers rather than quantitative measures.

Downstream staging should preserve their identifier semantics. A normalized representation may choose string types where canonical formatting or zero-padding is useful.

### District

`district` is numerically stored but semantically identifies a congressional district.

Observed values range from `0` through `53`.

`district = 0` is used for at-large/statewide congressional representation. It appears historically in:

* Alaska
* Delaware
* District of Columbia
* Montana
* Nevada
* North Dakota
* South Dakota
* Vermont
* Wyoming

District numbers should not be interpreted as stable geographic entities across the full historical period without incorporating congressional boundary/redistricting context.

### Version

`version = 20250910` is constant across the inspected source.

The value has `YYYYMMDD` form and should be treated as version/date metadata rather than a quantitative integer.

## Nullability

No SQL `NULL` values were observed in any of the 20 source columns.

This does **not** mean the source has no missing or unavailable information.

Several fields use literal or sentinel values instead:

* `runoff = 'NA'`
* `party = 'NA'`
* `candidatevotes = -1`
* `totalvotes = -1`

These values must remain distinguishable from actual SQL `NULL` during raw ingestion.

## Distinct / Categorical Values

### `year`

* Nulls: `0`
* Distinct values: `25`
* Range: 1976–2024
* Election years occur on a two-year cadence

### `state`

* Nulls: `0`
* Distinct values: `51`
* 50 states + District of Columbia

### `state_po`

* Nulls: `0`
* Distinct values: `51`

### `state_fips`

* Nulls: `0`
* Distinct values: `51`
* One mapping per state/DC

### `state_cen`

* Nulls: `0`
* Distinct values: `51`
* One mapping per state/DC

### `state_ic`

* Nulls: `0`
* Distinct values: `51`
* One mapping per state/DC

### `office`

* Nulls: `0`
* Distinct values: `1`
* `US HOUSE`: `33,805`

### `district`

* Nulls: `0`
* Distinct values: `54`
* Range: `0–53`
* `district = 0`: `669` rows

### `stage`

* Nulls: `0`
* `GEN`: `33,745`
* `PRI`: `60`

### `runoff`

Raw values when explicitly read as `VARCHAR`:

* Nulls: `0`
* `FALSE`: `25,141`
* `NA`: `8,656`
* `TRUE`: `8`

`NA` appears only in general-election rows from 2006–2018.

### `special`

* Nulls: `0`
* `FALSE`: `33,715`
* `TRUE`: `90`

### `candidate`

* Nulls: `0`
* Distinct raw values: `16,975`

The field contains both candidate names and non-person reporting categories.

### `party`

* Nulls: `0`
* Distinct raw values: `500`
* Literal `NA`: `4,094`

The raw vocabulary includes national parties, minor parties, historical/local party labels, affiliation-status labels, write-in labels, and spelling variation.

### `writein`

* Nulls: `0`
* `FALSE`: `30,956`
* `TRUE`: `2,849`

### `mode`

* Nulls: `0`
* `TOTAL`: `33,805`

### `candidatevotes`

* Nulls: `0`
* Minimum: `-1`
* Maximum: `387,109`

### `totalvotes`

* Nulls: `0`
* Minimum: `-1`
* Maximum: `656,104`

### `unofficial`

* Nulls: `0`
* `FALSE`: `33,766`
* `TRUE`: `39`

All observed `TRUE` values occur in 2018:

* North Carolina: `32`
* West Virginia: `7`

### `version`

* Nulls: `0`
* Distinct values: `1`
* `20250910`: `33,805`

### `fusion_ticket`

* Nulls: `0`
* `FALSE`: `31,128`
* `TRUE`: `2,677`

Multi-party candidates consistently had at least one associated result row with `fusion_ticket = TRUE` in the inspected source.

## Grain

Observed source grain:

> One candidate-party result line within a specific House election event.

Election-event fields:

```text
year
state
district
stage
runoff
special
```

Result-line fields generally include:

```text
candidate
party
writein
mode
```

Fusion voting intentionally creates multiple rows for the same candidate under different party labels.

Generic write-in reporting is an exception to normal descriptive uniqueness: multiple `WRITEIN / NA` rows may exist within the same event and differ only in their vote totals.

## Schema Notes

### File Delimiter

The downloaded source is named:

```text
1976-2024-house.tab
```

but its actual content is comma-delimited.

Explicitly parsing the file as tab-separated produces one giant column. DuckDB's automatic delimiter detection correctly parses the file as comma-separated.

### `runoff` Type Inference

DuckDB initially infers `runoff` as `BOOLEAN`.

This inference is unsafe because the raw field contains the literal string `NA`.

The first observed parsing failure occurred when DuckDB encountered an `NA` value outside its initial inference sample.

Raw inspection should therefore explicitly override:

```text
runoff → VARCHAR
```

until source-standardization rules are defined.

### Candidate and Party Semantics

Neither `candidate` nor `party` should be assumed to contain normalized entities.

`candidate` includes reporting categories in addition to person names.

`party` contains 500 raw labels and includes historical, local, write-in, affiliation-status, and inconsistent spellings.

Raw values should be preserved before downstream classification or normalization.

### Fusion Voting

A candidate may legitimately appear on several result rows with different party labels.

Votes on each party line are stored separately in `candidatevotes`.

Candidate-level aggregation therefore requires combining appropriate party lines rather than assuming one source row equals one candidate.

### `totalvotes`

`totalvotes` should not be assumed to be perfectly functionally dependent on the election-event fields.

Observed exceptions include:

* write-in rows carrying totals that include write-in votes while named-candidate rows exclude them
* ballot/reporting categories such as `BLANK` and `VOID` that are stored as result rows but excluded from `totalvotes`
* write-in normalization that can make row-level candidate vote sums differ from `totalvotes`
* ranked-choice-election values that require election-specific interpretation
* sentinel `-1` values

## Initial Type Considerations

These are staging considerations, not raw-ingestion transformations.

* Preserve the raw file unchanged.
* Preserve `runoff` as `VARCHAR` until the meaning of `NA` is formally standardized.
* Preserve literal `NA` independently from SQL `NULL`.
* Treat `state_fips`, `state_cen`, `state_ic`, and `district` as identifiers even if physically stored as integers.
* Consider deriving a true date from `version` while retaining the raw value.
* Preserve raw `candidate` and `party` strings before normalization.
* Do not blindly convert `candidatevotes = -1` or `totalvotes = -1` until the source sentinel convention is explicitly defined.
* Do not use `candidatevotes` as part of a natural key simply because it resolves generic write-in collisions.
* If a stable row identifier is required downstream, use a surrogate identifier or deterministic row hash rather than forcing a measure into the natural key.





Similarities
- Both are MEDSL / Harvard Dataverse sources.
- Both preserve raw candidate and party reporting labels.
- Both contain non-person values in candidate-like fields.
- Both require care around source sentinel values.
- Both use candidatevotes and totalvotes as central measures.
- Both have version metadata.
- Neither should be normalized destructively during raw ingestion.
- Both need source-specific staging before eventual cross-dataset standardization.


Presidential
- county-level
- county_fips has unusual/sentinel identifier behavior
- candidatevotes required VARCHAR because of literal NA
- mode has multiple/inconsistent values

House
- district-level
- several state coding systems
- district = 0 for at-large reporting
- stage/runoff/special/writein/unofficial/fusion_ticket
- candidatevotes is numeric but has a -1 sentinel
- mode is constant TOTAL
- fusion and generic write-in rows complicate grain