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

| Column           | Source Type              | DuckDB Type                     | Description                                       | Notes                                                                              |
| ---------------- | ------------------------ | ------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `year`           | Integer                  | `BIGINT`                        | Election year                                     | 25 distinct even-numbered election years from 1976–2024                            |
| `state`          | Text                     | `VARCHAR`                       | State name                                        | 51 uppercase values: 50 states + District of Columbia                              |
| `state_po`       | Text                     | `VARCHAR`                       | U.S. postal abbreviation                          | 51 two-character uppercase values                                                  |
| `state_fips`     | Identifier               | `BIGINT`                        | State FIPS code                                   | Numeric in source but semantically an identifier                                   |
| `state_cen`      | Identifier               | `BIGINT`                        | Census state identifier                           | Numeric in source but semantically an identifier                                   |
| `state_ic`       | Identifier               | `BIGINT`                        | State coding identifier                           | Numeric in source but semantically an identifier                                   |
| `office`         | Text                     | `VARCHAR`                       | Office being contested                            | Constant value: `US HOUSE`                                                         |
| `district`       | Identifier               | `BIGINT`                        | Congressional district number                     | Values 0–53; `0` used for at-large/statewide reporting                             |
| `stage`          | Categorical              | `VARCHAR`                       | Election stage                                    | Observed values: `GEN`, `PRI`                                                      |
| `runoff`         | Boolean-like categorical | Auto-inferred `BOOLEAN`; unsafe | Runoff-status field                               | Raw values are `TRUE`, `FALSE`, and literal `NA`; should be inspected as `VARCHAR` |
| `special`        | Boolean                  | `BOOLEAN`                       | Indicates special-election status                 | Clean Boolean field                                                                |
| `candidate`      | Text                     | `VARCHAR`                       | Candidate or source reporting label               | Includes person names and non-person reporting categories                          |
| `party`          | Text                     | `VARCHAR`                       | Party associated with result line                 | 500 raw labels including literal `NA` and historical/local labels                  |
| `writein`        | Boolean                  | `BOOLEAN`                       | Indicates write-in result line                    | Clean Boolean field                                                                |
| `mode`           | Categorical              | `VARCHAR`                       | Voting/reporting mode                             | Constant value: `TOTAL`                                                            |
| `candidatevotes` | Integer measure          | `BIGINT`                        | Votes associated with candidate-party result line | Contains a `-1` sentinel                                                           |
| `totalvotes`     | Integer measure          | `BIGINT`                        | Reported election-event vote total                | Contains `-1` sentinel values and several source-specific edge cases               |
| `unofficial`     | Boolean                  | `BOOLEAN`                       | Indicates unofficial results                      | `TRUE` occurs only in 2018 North Carolina and West Virginia                        |
| `version`        | Date-like metadata       | `BIGINT`                        | Source version/finalization stamp                 | Constant `20250910`; semantically metadata rather than a measure                   |
| `fusion_ticket`  | Boolean                  | `BOOLEAN`                       | Identifies fusion/cross-endorsed party lines      | Row-level flag associated with multi-party candidacies                             |

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

Inspection did not identify evidence requiring another event-level field.

Differences in `totalvotes` within some of these groups were traced to source/reporting conventions rather than distinct election events.

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

Observed row grain:

> One row represents one candidate-party result line within a specific U.S. House election event.

This requires an important qualification: generic `WRITEIN` rows can repeat with identical descriptive fields while carrying different `candidatevotes`.

The available descriptive fields therefore do not form a universally reliable natural key.

### Exact Duplicate Check

No exact duplicate rows were found when comparing all 20 source columns.

## Identifier Handling

### `state_fips`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Values are consistent with state FIPS codes
* Semantically an identifier rather than a numeric measure
* Likely downstream type: `VARCHAR`

### `state_cen`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Appears to be a Census state identifier
* Semantically an identifier rather than a numeric measure
* Exact field definition should remain tied to the source codebook

### `state_ic`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Appears to be a state identifier/coding scheme
* Semantically an identifier rather than a numeric measure
* Exact field definition should remain tied to the source codebook

### `district`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `54`
* Observed range: `0–53`
* `0` is used for statewide / at-large reporting
* Semantically a geographic identifier rather than a numeric measure
* District numbering changes historically as congressional apportionment changes

Observed states/DC using `district = 0` include:

* Alaska
* Delaware
* District of Columbia
* Montana
* Nevada
* North Dakota
* South Dakota
* Vermont
* Wyoming

District numbers should not be treated as stable geographic entities across the full historical period without incorporating congressional boundary/redistricting context.

### `version`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Distinct values: `1`
* Observed value: `20250910`
* Constant across all `33,805` rows
* Looks like a `YYYYMMDD`-style version stamp
* Semantically metadata rather than a numeric measure

## Nullability

No SQL `NULL` values were observed in any of the 20 source columns.

This does **not** mean the source contains no missing, unavailable, or non-applicable information.

Several fields instead use literal or sentinel values, including:

```text
runoff = 'NA'
party = 'NA'
candidatevotes = -1
totalvotes = -1
```

These values must remain distinguishable from actual SQL `NULL` during raw ingestion and staging.

## Distinct / Categorical Values

### `year`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `25`
* Range: `1976–2024`
* Observed values follow a two-year election cadence

### `state`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `51`
* Includes the 50 states plus District of Columbia
* Values are consistently uppercase

### `state_po`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `51`
* Two-character uppercase postal abbreviations
* Includes the 50 states plus DC

### `state_fips`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Values are consistent with state FIPS codes
* Semantically an identifier rather than a numeric measure
* Likely downstream type: `VARCHAR`

### `state_cen`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Appears to be a Census state identifier
* Semantically an identifier rather than a numeric measure
* Exact field definition should be confirmed against the source codebook

### `state_ic`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `51`
* One value per state/DC
* Appears to be a state identifier/coding scheme
* Semantically an identifier rather than a numeric measure
* Exact field definition should be confirmed against the source codebook

### `office`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `1`
* Observed value: `US HOUSE`
* Constant across the dataset
* `US HOUSE`: `33,805` rows

### `district`

* DuckDB type: `BIGINT`
* Null count: `0`
* Distinct values: `54`
* Observed range: `0–53`
* `district = 0`: `669` rows
* `0` is used for statewide / at-large reporting
* District numbering changes historically as congressional apportionment changes
* Semantically a geographic identifier rather than a numeric measure

### `stage`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `2`
* `GEN`: `33,745` rows
* `PRI`: `60` rows
* Appears to distinguish general and primary election records

### `runoff`

* Raw inspection type: `VARCHAR`
* SQL null count: `0`
* Distinct raw values: `TRUE`, `FALSE`, `NA`
* `FALSE`: `25,141`
* `NA`: `8,656`
* `TRUE`: `8`
* `NA` is a literal source value, not SQL `NULL`
* `NA` is concentrated in `GEN` rows from 2006–2018
* `TRUE` appears in four district-year contests
* DuckDB Boolean auto-inference is unsafe for this column
* Exact semantic meaning of `NA` still requires source-codebook confirmation

Observed `TRUE` records occur in:

```text
1996 Texas District 8
1996 Texas District 9
1996 Texas District 25
2002 Louisiana District 5
```

### `special`

* DuckDB type: `BOOLEAN`
* Null count: `0`
* Distinct values: `false`, `true`
* `false`: `33,715`
* `true`: `90`
* Clean Boolean field

### `candidate`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `16,975`
* Contains person names plus non-person reporting categories
* Should not be treated as a clean candidate dimension without downstream classification or normalization

Observed non-person values include:

```text
WRITEIN
OTHER
BLANK
BLANK VOTE
BLANK VOTE/SCATTERING
SCATTERING
VOID
UNDERVOTES
```

### `party`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct raw values: `500`
* Literal `NA`: `4,094` rows
* Literal `NA` is a source value, not SQL `NULL`
* Contains major parties, minor parties, local/historical labels, affiliation-status labels, write-in labels, and spelling variation
* Raw source vocabulary should be preserved before downstream normalization

Observed examples include:

```text
DEMOCRAT
REPUBLICAN
LIBERTARIAN
INDEPENDENT
CONSERVATIVE
GREEN
WORKING FAMILIES
NA
NONE
NO PARTY
NO PARTY AFFILIATION
UNAFFILIATED
WRITE-IN
```

### `writein`

* DuckDB type: `BOOLEAN`
* Null count: `0`
* Distinct values: `2`
* `false`: `30,956`
* `true`: `2,849`
* Clean Boolean field

### `mode`

* DuckDB type: `VARCHAR`
* Null count: `0`
* Distinct values: `1`
* Observed value: `TOTAL`
* Constant across all `33,805` rows

### `candidatevotes`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Minimum: `-1`
* Maximum: `387,109`
* `-1` occurs in exactly one row
* `-1` should be treated as a source sentinel rather than a literal negative vote count
* Exact sentinel semantics should still be confirmed against the MEDSL codebook

Observed negative row:

```text
2020 Florida District 25
candidatevotes = -1
totalvotes = -1
```

### `totalvotes`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Minimum: `-1`
* Maximum: `656,104`
* `-1` occurs in `3` rows
* Observed negative values appear to be sentinel values rather than literal vote totals
* Sentinel behavior differs somewhat from `candidatevotes`
* Exact source convention should still be confirmed against the MEDSL codebook

Observed `totalvotes = -1` rows:

```text
2020 Florida District 25
2024 Florida District 20
2024 Oklahoma District 3
```

### `unofficial`

* DuckDB type: `BOOLEAN`
* SQL null count: `0`
* Distinct values: `false`, `true`
* `false`: `33,766`
* `true`: `39`
* `TRUE` appears only in 2018
* `TRUE` rows are limited to North Carolina and West Virginia
* Exact source definition should remain tied to the codebook

Observed distribution:

```text
2018 North Carolina: 32
2018 West Virginia:   7
```

### `version`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Distinct values: `1`
* Observed value: `20250910`
* Constant across all `33,805` rows
* Looks like a `YYYYMMDD`-style version stamp
* Semantically metadata rather than a numeric measure

### `fusion_ticket`

* DuckDB type: `BOOLEAN`
* SQL null count: `0`
* Distinct values: `false`, `true`
* `false`: `31,128`
* `true`: `2,677`
* Clean Boolean field syntactically
* Exact MEDSL definition should remain tied to the source codebook
* Observed behavior shows that the flag operates at the result-line level rather than necessarily being `TRUE` for every party line associated with a multi-party candidate
* Every inspected non-write-in candidate appearing under multiple party labels had at least one associated row where `fusion_ticket = TRUE`

## Grain

Observed source grain:

> One candidate-party result line within a specific House election event.

### Election-Event Fields

The working event-level combination is:

```text
year
state
district
stage
runoff
special
```

`year + state + district` alone is insufficient.

For example, 1996 Texas District 25 contains both:

```text
PRI + special = TRUE + runoff = FALSE
```

and:

```text
GEN + special = FALSE + runoff = TRUE
```

within the same district-year.

### Result-Line Fields

For normal non-write-in records, result-line identity is described by:

```text
candidate
party
writein
mode
```

in addition to the election-event fields.

### Fusion Voting

The same candidate can legitimately appear on multiple result rows under different party labels.

Example: 2018 New York District 2 contains Peter T. King on five separate party lines.

Each line has its own `candidatevotes`.

Therefore:

```text
one row != one unique candidate/person
```

Candidate-level aggregation may require combining multiple party-line rows.

### Generic Write-In Exception

Generic `WRITEIN` reporting prevents the descriptive fields from forming a universal natural key.

The tested descriptive key:

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

produced `85` collision groups.

All observed collisions were write-in records.

When `writein = FALSE`, the same descriptive combination produced `0` collisions.

Example: 2008 Maryland District 4 contains four rows with:

```text
candidate = WRITEIN
party = NA
writein = TRUE
mode = TOTAL
```

but different `candidatevotes`:

```text
28
48
75
453
```

Adding `candidatevotes` makes those rows unique, but `candidatevotes` is a measure and should not be incorporated into a natural key solely to force uniqueness.

### Exact Duplicate Rows

Grouping by all 20 source columns produced:

```text
0 exact duplicate rows
```

Every physical row in the inspected source is therefore unique.

## Schema Notes

### File Delimiter

The downloaded source is named:

```text
1976-2024-house.tab
```

but its actual content is comma-delimited.

Explicit parsing with `delim='\t'` causes the entire header to be interpreted as one column.

DuckDB correctly parses the file using:

```python
read_csv_auto(house_path)
```

without forcing the delimiter.

The ingestion layer should therefore not assume that the source extension or Dataverse format label reliably identifies the physical delimiter.

### `runoff` Type Inference

DuckDB initially infers:

```text
runoff → BOOLEAN
```

based on its sampling.

That inference is unsafe because later rows contain the literal string:

```text
NA
```

which cannot be converted to Boolean.

Raw inspection therefore requires:

```python
types={'runoff': 'VARCHAR'}
```

until a deliberate standardization rule is defined.

### Candidate Semantics

`candidate` should not be interpreted as a normalized candidate entity.

The column contains:

* candidate names
* generic write-in labels
* blank-vote categories
* scattering categories
* void-vote categories
* undervote categories
* other source reporting labels

A downstream candidate dimension will require classification before assuming that a row represents a person.

### Party Semantics

`party` should not be interpreted as a normalized party dimension.

The source contains `500` distinct raw labels including:

* major parties
* minor parties
* historical parties
* local parties
* affiliation-status labels
* write-in labels
* spelling variation
* literal `NA`

The raw value should be preserved separately from any standardized party classification.

### Fusion / Cross-Endorsed Results

A candidate may appear under multiple party labels in the same election event.

Votes are preserved on separate result lines.

The `fusion_ticket` field is row-level:

* a base party line may be `FALSE`
* one or more additional party lines may be `TRUE`

Candidate-level aggregation must therefore account for multiple party lines rather than assuming one source row per candidate.

### `candidatevotes`

`candidatevotes` is a result-line measure.

It should not be used as part of a natural key solely because adding it resolves generic write-in collisions.

A stable downstream row identifier should instead use a surrogate key, source row identifier if one becomes available, or deterministic row hash.

### `totalvotes`

`totalvotes` should not be assumed to be perfectly functionally dependent on the event fields or equal to a simple sum of all `candidatevotes`.

Observed reasons include:

* write-in rows whose `totalvotes` includes write-in votes while named-candidate rows exclude them
* `BLANK` and `VOID` reporting categories whose counts are stored as result rows but excluded from `totalvotes`
* generic write-in normalization that can prevent row-level vote sums from reproducing `totalvotes`
* ranked-choice-election edge cases
* `-1` sentinel values

#### 2018 Georgia Write-In Behavior

Five 2018 Georgia districts contained two `totalvotes` values within the same election event:

```text
Districts 6, 8, 9, 12, 13
```

In every case:

```text
write-in row total
=
named-candidate total + write-in candidatevotes
```

Example:

```text
GA-06
named-candidate total = 317014
write-in votes        =     18
write-in row total    = 317032
```

This is a source/reporting convention rather than evidence of a second election event.

#### 2024 New York

The source contains categories such as:

```text
BLANK
VOID
SCATTERING
```

For 2024 New York House contests, `BLANK` and `VOID` values are represented in `candidatevotes` rows but excluded from `totalvotes`.

For New York District 1:

```text
SUM(all candidatevotes) = 430460
BLANK                    =  19984
VOID                     =    376
totalvotes               = 410100
```

Excluding `BLANK` and `VOID` produces exactly:

```text
410100
```

`SCATTERING` remains included.

The same rule resolved the inspected 2024 New York district mismatches.

#### 2024 Maine District 1

The source contains:

```text
BLANK = 14037
```

Votes for the three actual candidate lines sum exactly to:

```text
425530
```

which matches `totalvotes`.

The additional `BLANK` row should therefore not be included when reconstructing the candidate-vote total for the contest.

#### Generic Write-In Normalization

Some contests show evidence that distinct write-in candidates in underlying results have been normalized to generic:

```text
WRITEIN
```

rows.

Observed cases include:

```text
2002 Indiana District 2
2012 Connecticut District 3
2016 Connecticut District 1
```

In these cases, `SUM(candidatevotes)` falls slightly short of `totalvotes`.

Generic write-in representation should therefore be treated as potentially lossy.

#### 2018 Maine District 2

Observed values:

```text
JARED F GOLDEN   139231
BRUCE POLIQUIN   136326

SUM(candidatevotes) = 275557
totalvotes          = 281371
```

This ranked-choice contest does not behave like a normal plurality-election result.

The source values appear to represent different ranked-choice tabulation states or stages and require election-specific interpretation before downstream analytical use.

## Initial Type Considerations

These are staging/modeling considerations rather than raw-ingestion transformations.

* Preserve the downloaded raw source unchanged.
* Preserve raw strings and source-specific sentinel values before normalization.
* Read `runoff` as `VARCHAR` during raw parsing rather than trusting automatic Boolean inference.
* Keep literal `NA` distinct from SQL `NULL`.
* Consider representing `state_fips`, `state_cen`, `state_ic`, and `district` as identifier-oriented string fields downstream even though the source parses them as integers.
* Preserve the original `version` value and optionally derive a proper date field separately.
* Preserve raw `candidate` before classifying candidate names versus reporting categories.
* Preserve raw `party` before applying any standardized party mapping.
* Treat `candidatevotes` and `totalvotes` as numeric measures with source-specific sentinel and aggregation behavior.
* Do not automatically convert `-1` to a particular semantic meaning until the source convention is formally confirmed.
* Do not use `candidatevotes` as part of a natural key merely because it resolves generic write-in collisions.
* Do not assume `SUM(candidatevotes) = totalvotes` without accounting for reporting categories and election-specific behavior.
* Candidate-level analysis must account for fusion/cross-endorsed party lines.
* Generic `WRITEIN` rows require special treatment because the source may not preserve enough descriptive information to distinguish all underlying write-in candidates.
* If downstream models require guaranteed row identity, use a surrogate key or deterministic row hash rather than forcing measures into the natural key.
