# Source Schema

## Source File

* Dataset: `MIT County Presidential Returns 2000–2024`
* File: `countypres_2000-2024.csv`
* Format: `CSV`
* Source: `MIT Election Data and Science Lab / Harvard Dataverse`
* Coverage: `U.S. presidential election returns by county, 2000–2024`

Because CSV does not enforce column types, the types below are those inferred by DuckDB during raw-source inspection.

## Columns

| Column           | Source Type | DuckDB Type | Description                              | Notes                                         |
| ---------------- | ----------- | ----------- | ---------------------------------------- | --------------------------------------------- |
| `state`          | CSV field   | `VARCHAR`   | State name                               | 51 distinct values; no SQL nulls              |
| `county_name`    | CSV field   | `VARCHAR`   | County or reporting-geography name       | 1,921 distinct values; no SQL nulls           |
| `year`           | CSV field   | `BIGINT`    | Election year                            | 7 distinct values                             |
| `state_po`       | CSV field   | `VARCHAR`   | State postal abbreviation                | 51 distinct values                            |
| `county_fips`    | CSV field   | `VARCHAR`   | County FIPS or geographic identifier     | Contains literal `NA` and nonstandard lengths |
| `office`         | CSV field   | `VARCHAR`   | Office contested                         | Single value: `US PRESIDENT`                  |
| `candidate`      | CSV field   | `VARCHAR`   | Candidate or vote-category label         | Includes non-person categories                |
| `party`          | CSV field   | `VARCHAR`   | Candidate party                          | 501 SQL nulls                                 |
| `candidatevotes` | CSV field   | `VARCHAR`   | Votes associated with candidate/category | Semantically numeric; contains literal `NA`   |
| `totalvotes`     | CSV field   | `BIGINT`    | Total votes cast in county-year          | Numeric throughout inspected source           |
| `version`        | CSV field   | `BIGINT`    | Dataset finalization date                | Encoded as `YYYYMMDD`                         |
| `mode`           | CSV field   | `VARCHAR`   | Ballot/reporting mode                    | 2,795 SQL nulls; vocabulary varies            |

> Distinct counts exclude SQL `NULL` values.

## Key Fields

No universally reliable natural key was identified in the raw source.

The following combination was tested as a likely natural key:

* `year`
* `state_po`
* `county_fips`
* `office`
* `candidate`
* `party`
* `mode`

This combination uniquely identifies records for election years `2000–2020`, but does not uniquely identify all records in `2024`.

Adding `county_name` does not resolve the 2024 collisions.

The observed collisions are isolated to North Carolina, South Carolina, California, Arizona, and Connecticut and are associated with multiple source-standardization issues.

Detailed collision analysis is documented in [Data Quality Findings](./data_quality_findings.md).

## Identifier Handling

### `county_fips`

`county_fips` must be treated as a string identifier rather than a numeric measure.

Observed characteristics:

* DuckDB type: `VARCHAR`
* SQL null count: `0`
* Literal `NA` count: `52`
* Distinct values: `3,158`

Observed lengths excluding `NA`:

| Length |   Rows |
| -----: | -----: |
|      4 | 10,858 |
|      5 | 83,220 |
|      7 |     21 |

Standard state + county FIPS identifiers are expected to contain five characters.

Four-character values appear consistent with loss of a leading zero.

One seven-character value was observed:

```text
2938000
```

Literal `NA` occurs on special reporting records including:

* `STATEWIDE WRITEIN`
* `MAINE UOCAVA`
* `FEDERAL PRECINCT`

These values should not automatically be interpreted as erroneous missing data.

The source codebook separately documents special handling for Alaska in 2004.

Additional geographic anomalies are documented in [Data Quality Findings](./data_quality_findings.md).

### Candidate Identifiers

The `candidate` field should not be treated as a normalized person identifier.

The field contains both candidate names and non-person vote categories, including:

* `OTHER`
* `OVERVOTES`
* `UNDERVOTES`
* `SPOILED`
* `TOTAL VOTES CAST`

Candidate naming also varies across election cycles. For example:

```text
DONALD TRUMP
DONALD J TRUMP
```

Normalization should occur downstream rather than modifying the raw source.

## Nullability

The raw source uses both SQL `NULL` values and literal `NA` strings to represent missing or non-applicable values.

| Column           | Representation | Count | Observation                                    |
| ---------------- | -------------- | ----: | ---------------------------------------------- |
| `party`          | SQL `NULL`     |   501 | Occurs only on non-candidate/status records    |
| `mode`           | SQL `NULL`     | 2,795 | All observed nulls occur in 2024               |
| `county_fips`    | Literal `NA`   |    52 | Occurs on special/non-county reporting records |
| `candidatevotes` | Literal `NA`   |    37 | Field is otherwise numeric                     |

No SQL `NULL` values were observed in the other inspected columns.

No literal `NA` values were observed in the other inspected string columns.

### `party`

All observed `party` nulls are associated with non-candidate/status records:

| Candidate/category | Null-party rows |
| ------------------ | --------------: |
| `TOTAL VOTES CAST` |             427 |
| `UNDERVOTES`       |              37 |
| `OVERVOTES`        |              23 |
| `SPOILED`          |              14 |

These nulls therefore appear semantically appropriate rather than representing missing party information for named candidates.

### `mode`

* SQL null count: `2,795`
* All observed null values occur in election year `2024`
* No null `mode` values were observed from `2000–2020`

The 2024 behavior should be handled explicitly during downstream staging design.

## Distinct / Categorical Values

### `state`

* 51 distinct values
* Full uppercase state names
* Contains the 50 states plus the District of Columbia
* No missing values or obvious formatting inconsistencies observed

### `county_name`

* 1,921 distinct values
* No missing values observed
* `county_name` alone should not be assumed to uniquely identify a geography

### `year`

Observed values:

* `2000`
* `2004`
* `2008`
* `2012`
* `2016`
* `2020`
* `2024`

Additional observations:

* Minimum: `2000`
* Maximum: `2024`
* Seven distinct values
* No missing or unexpected values observed

### `state_po`

* 51 distinct values
* Two-character uppercase postal abbreviations
* Includes the 50 states plus `DC`
* No missing values or obvious formatting inconsistencies observed

### `office`

* Single observed value: `US PRESIDENT`
* No missing values
* No formatting variants observed
* Constant across the dataset

### `candidate`

* 19 distinct values
* No missing values
* Contains both candidate names and non-person vote categories

### `party`

Five distinct non-null values were observed:

* `DEMOCRAT`
* `GREEN`
* `LIBERTARIAN`
* `OTHER`
* `REPUBLICAN`

### `mode`

* 19 distinct non-null values
* Vocabulary is not fully standardized

Several labels appear semantically related:

```text
EARLY
EARLY VOTE
EARLY VOTING
```

```text
MAIL
MAIL-IN
ABSENTEE BY MAIL
```

```text
PROV
PROVISIONAL
```

Normalization requirements should be determined during staging design rather than applied to the raw source.

## Grain

### Expected Grain

One row appears intended to represent one candidate or vote category within a combination of:

* presidential election year
* state
* county/reporting geography
* party
* ballot/reporting mode

### Grain Validation

The tested natural-key candidate uniquely identifies rows for `2000–2020` but not for all `2024` records.

Because the source contains special reporting geographies, category records, inconsistent geographic identifiers, and 2024 key collisions, the raw dataset should not currently be assumed to have a universally valid natural key.

See [Data Quality Findings](./data_quality_findings.md) for detailed investigation.

## Schema Notes

### `candidatevotes`

* DuckDB type: `VARCHAR`
* SQL null count: `0`
* Distinct values: `22,108`
* Literal `NA` count: `37`
* Other non-numeric values: `0`

Every non-`NA` value inspected can be cast to `BIGINT`.

The field is semantically numeric, but literal `NA` values cause DuckDB to infer the raw field as `VARCHAR`.

Downstream modeling will likely need to handle `NA` before casting to a numeric type.

### `totalvotes`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Distinct values: `16,846`
* All observed values are numeric
* No obvious structural or formatting issues observed

### `version`

* DuckDB type: `BIGINT`
* SQL null count: `0`
* Distinct values: `1`
* Observed value: `20260225`
* Encoded in `YYYYMMDD` form

The field is semantically a date rather than a numeric measure and is a likely candidate for conversion to `DATE` downstream.

## Initial Type Considerations

These are observations for future staging design. No source values are modified during raw-data inspection.

| Column           | Raw Type  | Likely Analytical Type | Reason                                      |
| ---------------- | --------- | ---------------------- | ------------------------------------------- |
| `county_fips`    | `VARCHAR` | `VARCHAR`              | Geographic identifier; leading zeros matter |
| `candidatevotes` | `VARCHAR` | nullable `BIGINT`      | Semantically numeric; source contains `NA`  |
| `version`        | `BIGINT`  | `DATE`                 | Encoded as `YYYYMMDD`                       |

Raw source values remain unchanged during the discovery and ingestion phases.
