# Source Schema

## Source File

**Dataset:** U.S. Senate statewide 1976–2024
**Source:** MIT Election Data and Science Lab / Harvard Dataverse
**Dataset DOI:** `doi:10.7910/DVN/PEJ5QU`
**Dataset ID:** `3072248`
**Dataset version:** `8.0`
**Release date:** `2026-05-11`

**Target file**

* Original name: `1976-2024-senate-state.csv`
* File ID: `13887039`
* Original size: `530501` bytes
* Checksum type: `MD5`
* Checksum: `0f8b51cf0f77a2ef0bff992f7a64d1b4`
* Observed row count: `3,945`
* Observed column count: `19`

The source file is CSV and does not enforce database-level types. The inferred types below are the types produced by DuckDB `read_csv_auto()`.

## Columns

| Column             | Source Type       | Inferred Type | Description                                                      | Notes                                                                               |
| ------------------ | ----------------- | ------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `year`             | Unspecified (CSV) | BIGINT        | Election year recorded by the source                             | 26 distinct years spanning 1976–2024                                                |
| `state`            | Unspecified (CSV) | VARCHAR       | Full state name                                                  | 50 distinct states; no D.C.                                                         |
| `state_po`         | Unspecified (CSV) | VARCHAR       | State postal abbreviation                                        | 50 distinct two-character uppercase values                                          |
| `state_fips`       | Unspecified (CSV) | BIGINT        | State FIPS identifier                                            | 50 distinct values; range 1–56; one value per state                                 |
| `state_cen`        | Unspecified (CSV) | DOUBLE        | Census state identifier                                          | 50 distinct values; all observed values are integer-valued despite DOUBLE inference |
| `state_ic`         | Unspecified (CSV) | BIGINT        | ICPSR-style state identifier supplied by source                  | 50 distinct values; one value per state                                             |
| `office`           | Unspecified (CSV) | VARCHAR       | Office represented by the row                                    | Constant value `US SENATE`                                                          |
| `district`         | Unspecified (CSV) | VARCHAR       | Geographic election district                                     | Constant value `statewide`                                                          |
| `stage`            | Unspecified (CSV) | VARCHAR       | Source-provided election-stage label                             | Raw values are historically inconsistent and should be preserved                    |
| `special`          | Unspecified (CSV) | BOOLEAN       | Indicates whether the election is a special election             | Required to distinguish some events occurring in the same state/year/stage          |
| `candidate`        | Unspecified (CSV) | VARCHAR       | Source-provided candidate or result label                        | Nullable; populated values are not guaranteed to represent a person                 |
| `party_detailed`   | Unspecified (CSV) | VARCHAR       | Detailed source party/affiliation label                          | Raw vocabulary contains 195 distinct non-null values                                |
| `writein`          | Unspecified (CSV) | BOOLEAN       | Indicates a write-in result line                                 | Includes both named and unnamed write-in results                                    |
| `mode`             | Unspecified (CSV) | VARCHAR       | Source reporting mode                                            | Only `total` and `TOTAL` observed                                                   |
| `candidatevotes`   | Unspecified (CSV) | DOUBLE        | Votes associated with the reported result line                   | No null or fractional values observed                                               |
| `totalvotes`       | Unspecified (CSV) | DOUBLE        | Total votes associated with the source-defined election grouping | Repeated across rows in the same working event group                                |
| `unofficial`       | Unspecified (CSV) | BOOLEAN       | Source flag indicating unofficial results                        | 21 rows are `true`                                                                  |
| `version`          | Unspecified (CSV) | VARCHAR       | Source revision/update metadata                                  | Multiple date-like formats occur                                                    |
| `party_simplified` | Unspecified (CSV) | VARCHAR       | Source-provided broad party classification                       | Preserved separately from `party_detailed`                                          |

## Key Fields

A useful **working election-event grouping** is:

```text
year
+ state
+ stage
+ special
```

This produces `862` observed event groups and generally groups related result lines correctly.

It is **not a universally unique real-world election-event key**. Louisiana 2002 contains multiple election rounds that share the same values for all four fields.

At the row level, the following observed combination is unique within the current file:

```text
year
+ state
+ stage
+ special
+ candidate
+ party_detailed
+ writein
+ mode
+ candidatevotes
```

However, `candidatevotes` is a measure rather than a stable identity attribute and should not be treated as a semantic natural key merely because including it produces uniqueness.

No reliable descriptive natural key has been identified for every source row.

## Identifier Handling

`state_fips`, `state_cen`, and `state_ic` should be treated as identifiers rather than quantitative measures.

Although `state_cen` is inferred as `DOUBLE`, all observed values are integer-valued.

Each of the three state identifier fields maps consistently to exactly one value per state in the current file.

Raw source values should be preserved during ingestion. Any downstream normalization or formatting of identifiers should occur in later staging/modeling layers rather than altering the raw source representation.

## Nullability

DuckDB `DESCRIBE` reports all columns as nullable because the CSV does not provide database constraints. This does **not** mean null values were observed in every column.

Observed null behavior includes:

| Column             | Observed null count | Notes                                                               |
| ------------------ | ------------------: | ------------------------------------------------------------------- |
| `candidate`        |                 423 | All observed null-candidate rows are write-in rows                  |
| `party_detailed`   |                 627 | Includes write-ins, reporting categories, and some named candidates |
| `party_simplified` |                   2 | Both are non-party reporting categories                             |
| `year`             |                   0 |                                                                     |
| `state`            |                   0 |                                                                     |
| `state_po`         |                   0 |                                                                     |
| `state_fips`       |                   0 |                                                                     |
| `state_cen`        |                   0 |                                                                     |
| `state_ic`         |                   0 |                                                                     |
| `office`           |                   0 |                                                                     |
| `district`         |                   0 |                                                                     |
| `stage`            |                   0 |                                                                     |
| `special`          |                   0 |                                                                     |
| `writein`          |                   0 |                                                                     |
| `candidatevotes`   |                   0 |                                                                     |
| `totalvotes`       |                   0 |                                                                     |
| `unofficial`       |                   0 |                                                                     |
| `version`          |                   0 |                                                                     |

No null behavior was identified that requires modification during raw ingestion.

## Distinct / Categorical Values

### `year`

* Type: `BIGINT`
* Null count: `0`
* Distinct values: `26`
* Range: `1976–2024`
* Primarily even-numbered federal election years
* `2021` occurs for Georgia runoff records

### `state`

* Type: `VARCHAR`
* Null count: `0`
* Distinct values: `50`
* Coverage: all 50 states
* D.C. is not present

### `state_po`

* Type: `VARCHAR`
* Null count: `0`
* Distinct values: `50`
* Minimum length: `2`
* Maximum length: `2`
* Format: uppercase postal abbreviations

### `state_fips`

* Type: `BIGINT`
* Null count: `0`
* Distinct values: `50`
* Range: `1–56`
* Exactly one value observed per state

### `state_cen`

* Type: `DOUBLE`
* Null count: `0`
* Distinct values: `50`
* Range: `11.0–95.0`
* Fractional values: `0`
* Exactly one value observed per state

### `state_ic`

* Type: `BIGINT`
* Null count: `0`
* Distinct values: `50`
* Range: `1–82`
* Exactly one value observed per state

### `office`

* Type: `VARCHAR`
* Null count: `0`
* Distinct values: `1`
* Value: `US SENATE`

### `district`

* Type: `VARCHAR`
* Null count: `0`
* Distinct values: `1`
* Value: `statewide`

### `stage`

Five raw values are observed:

| Value        |  Rows |
| ------------ | ----: |
| `gen`        | 3,616 |
| `GEN`        |   314 |
| `pre`        |     9 |
| `runoff`     |     4 |
| `GEN RUNOFF` |     2 |

Observed temporal behavior:

* `gen`: 1976–2020
* `GEN`: 2022–2024
* `pre`: Georgia only, in 1992 and 2008
* `runoff`: Georgia only, in 2021
* `GEN RUNOFF`: Georgia only, in 2022

The raw encoding changes over time. `stage` should therefore be preserved as supplied rather than normalized during ingestion.

### `special`

* Type: `BOOLEAN`
* Null count: `0`
* `false`: 3,788 rows
* `true`: 157 rows
* `special = true` occurs across 29 year/state/stage groups
* 18 year/state/stage combinations contain both regular and special records

`special` is therefore required when distinguishing some Senate election events.

### `candidate`

* Type: `VARCHAR`
* Null count: `423`
* Distinct non-null values: `2,584`

All null-candidate rows are write-in rows and also have `party_detailed = NULL`.

Of the 472 total write-in rows:

* 423 have `candidate = NULL`
* 49 have a populated candidate value

A populated `candidate` value is not guaranteed to represent a person. For example, `SCATTER` occurs as a candidate value.

### `party_detailed`

* Type: `VARCHAR`
* Null count: `627`
* Distinct non-null values: `195`

The field contains:

* major-party labels
* minor-party labels
* historical-party labels
* affiliation/status labels
* combined or fusion labels
* reporting-related labels

Semantically similar values may have different raw encodings, such as `DEMOCRAT` and `DEMOCRATIC`.

This field should be preserved as raw source vocabulary during ingestion.

### `writein`

* Type: `BOOLEAN`
* Null count: `0`
* `false`: 3,473 rows
* `true`: 472 rows

Write-in rows include both named and unnamed result lines.

### `mode`

Two raw values are observed:

| Value   |  Rows | Years     |
| ------- | ----: | --------- |
| `total` | 3,629 | 1976–2021 |
| `TOTAL` |   316 | 2022–2024 |

The casing shift appears alongside other source-format changes beginning in 2022. Raw values should be preserved.

### `candidatevotes`

* Type: `DOUBLE`
* Null count: `0`
* Range: `1–9,036,252`
* Fractional values: `0`

Although inferred as `DOUBLE`, all observed values behave as whole-number vote counts.

### `totalvotes`

* Type: `DOUBLE`
* Null count: `0`
* Range: `1–15,348,846`
* Fractional values: `0`

Although inferred as `DOUBLE`, all observed values behave as whole-number vote counts.

### `unofficial`

* Type: `BOOLEAN`
* Null count: `0`
* `false`: 3,924 rows
* `true`: 21 rows

The 21 unofficial rows occur across 9 year/state/stage/special groups.

### `version`

* Type: `VARCHAR`
* Null count: `0`
* Distinct raw values: `4`

Observed values include both `YYYYMMDD` and `MM/DD/YY` formatting.

`version` can differ within the same election year. In 2024, regular-election rows use `11/20/25`, while California and Nebraska special-election rows use `20241212`.

The field should remain raw metadata rather than being interpreted as a numeric value.

### `party_simplified`

Observed values:

* `OTHER`
* `DEMOCRAT`
* `REPUBLICAN`
* `LIBERTARIAN`
* `NULL`

Only two rows contain a null `party_simplified` value, and both correspond to non-party reporting categories.

`party_simplified` is a source-provided broad classification and should remain distinct from `party_detailed`.

## Grain

The source contains `3,945` rows.

The working event grain is:

```text
year + state + stage + special
```

This produces `862` event groups.

Within every working event group:

* `totalvotes` has one distinct value
* `SUM(candidatevotes) = totalvotes`

The working grouping is useful but does not universally represent one distinct real-world election round.

The working **row grain** is:

> One reported candidate/result line within a Senate election event as represented by the source.

Important qualifications:

* unnamed write-in rows may share the same descriptive candidate and party fields
* Louisiana 2002 contains multiple election rounds that cannot be separated using the available event descriptors
* no exact duplicate raw rows were observed
* every raw row is distinct across the complete set of source columns
* descriptive fields alone do not provide a stable natural key for every row

## Schema Notes

* The source contains 19 columns and 3,945 observed rows.
* DuckDB schema nullability reflects CSV parsing and does not represent observed null counts.
* `candidatevotes` and `totalvotes` are inferred as `DOUBLE`, but no fractional values occur.
* `state_cen` is inferred as `DOUBLE`, but no fractional values occur.
* Several categorical fields exhibit historical formatting or coding changes.
* Raw values should be preserved during ingestion.
* Stage, party, mode, identifier, and election-event normalization should be deferred to a downstream staging/modeling layer.
