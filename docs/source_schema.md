# Source Schema

## Dataset

**Dataset:** MIT County Presidential Returns 2000–2024  
**File:** `countypres_2000-2024.csv`  
**Format:** CSV  
**Source:** MIT Election Data and Science Lab / Harvard Dataverse  
**Coverage:** U.S. presidential election returns by county, 2000–2024

---

## Raw Schema

| Column | DuckDB Type | Source Meaning | Null Count | Distinct Count |
|---|---|---|---:|---:|
| `state` | `VARCHAR` | State name | 0 | 51 |
| `county_name` | `VARCHAR` | County name | 0 | 1,921 |
| `year` | `BIGINT` | Election year | 0 | 7 |
| `state_po` | `VARCHAR` | State postal abbreviation | 0 | 51 |
| `county_fips` | `VARCHAR` | County FIPS code | 0 | 3,158 |
| `office` | `VARCHAR` | Office contested | 0 | 1 |
| `candidate` | `VARCHAR` | Candidate or vote-category label | 0 | 19 |
| `party` | `VARCHAR` | Candidate party | 501 | 5 |
| `candidatevotes` | `VARCHAR` | Votes associated with candidate/category | 0 | 22,108 |
| `totalvotes` | `BIGINT` | Total votes cast in county-year | 0 | 16,846 |
| `version` | `BIGINT` | Dataset finalization date | 0 | 1 |
| `mode` | `VARCHAR` | Ballot/reporting mode | 2,795 | 19 |

> Distinct counts exclude SQL `NULL` values.

---

## Row Grain

### Expected Grain

One row appears intended to represent one candidate or vote category within a:

- presidential election year
- state
- county/reporting geography
- party
- ballot mode

### Validation

The proposed identifying combination:

- `year`
- `state_po`
- `county_name`
- `county_fips`
- `office`
- `candidate`
- `party`
- `mode`

is unique for election years **2000–2020**.

The same combination is not unique for some records in **2024**.

The 2024 grain collisions have been isolated to North Carolina, South Carolina,
California, Arizona, and Connecticut and represent several different source
standardization issues.

See `data_quality_findings.md` for the detailed investigation.

---

## Column Profiles

### `state`

- Full uppercase state names
- 51 distinct values
- Contains the 50 states plus the District of Columbia
- No missing values or obvious formatting inconsistencies observed

### `county_name`

- 1,921 distinct county-name strings
- No missing values observed
- `county_name` alone should not be assumed to uniquely identify a geography

### `year`

- Observed values:
  - `2000`
  - `2004`
  - `2008`
  - `2012`
  - `2016`
  - `2020`
  - `2024`
- Minimum: `2000`
- Maximum: `2024`
- Follows the expected four-year presidential-election cadence
- No missing or unexpected values observed

### `state_po`

- 51 distinct values
- Two-character uppercase postal abbreviations
- Includes the 50 states plus `DC`
- No missing values or obvious formatting inconsistencies observed

### `county_fips`

- DuckDB type: `VARCHAR`
- SQL null count: `0`
- Literal `NA` count: `52`
- Distinct values: `3,158`

Observed lengths excluding `NA`:

| Length | Rows |
|---:|---:|
| 4 | 10,858 |
| 5 | 83,220 |
| 7 | 21 |

Observations:

- Standard state + county identifiers are expected to contain 5 characters.
- Four-character values appear consistent with loss of a leading zero.
- One 7-character value was observed: `2938000`.
- `NA` occurs on special reporting records including:
  - `STATEWIDE WRITEIN`
  - `MAINE UOCAVA`
  - `FEDERAL PRECINCT`
- Literal `NA` values should therefore not automatically be interpreted as
  erroneous missing data.
- The source codebook separately documents special handling for Alaska in 2004.

See `data_quality_findings.md` for geographic anomalies requiring further review.

### `office`

- Single observed value: `US PRESIDENT`
- No missing values
- No formatting variants observed
- Constant across the dataset

### `candidate`

- 19 distinct values
- No missing values
- Most values represent presidential candidates
- The field also contains non-person categories:
  - `OTHER`
  - `OVERVOTES`
  - `UNDERVOTES`
  - `SPOILED`
  - `TOTAL VOTES CAST`
- Therefore, the raw `candidate` field should not be modeled as strictly a
  person-name field.
- Candidate naming is not fully normalized across election cycles; for example:
  - `DONALD TRUMP`
  - `DONALD J TRUMP`

### `party`

- 501 SQL nulls
- 5 distinct non-null values:
  - `DEMOCRAT`
  - `GREEN`
  - `LIBERTARIAN`
  - `OTHER`
  - `REPUBLICAN`

All observed nulls are associated with non-candidate/status records:

| Candidate/category | Null-party rows |
|---|---:|
| `TOTAL VOTES CAST` | 427 |
| `UNDERVOTES` | 37 |
| `OVERVOTES` | 23 |
| `SPOILED` | 14 |

These nulls therefore appear semantically appropriate rather than representing
missing party information for named candidates.

### `candidatevotes`

- DuckDB type: `VARCHAR`
- SQL null count: `0`
- Distinct values: `22,108`
- Literal `NA` count: `37`
- Other non-numeric values: `0`

Observations:

- Every non-`NA` value can be cast to `BIGINT`.
- The literal `NA` values cause DuckDB to infer the entire field as `VARCHAR`.
- The field is semantically numeric.
- Downstream modeling will likely require handling `NA` before casting to a
  numeric type.

See `data_quality_findings.md` for investigation of the `NA` records.

### `totalvotes`

- DuckDB type: `BIGINT`
- Null count: `0`
- Distinct values: `16,846`
- All observed values are numeric
- No obvious structural or formatting issues observed

### `version`

- DuckDB type: `BIGINT`
- Null count: `0`
- Distinct values: `1`
- Observed value: `20260225`
- Stored in `YYYYMMDD` form
- Semantically represents a date rather than a numeric measure
- Likely candidate for conversion to `DATE` downstream

### `mode`

- DuckDB type: `VARCHAR`
- Null count: `2,795`
- Distinct non-null values: `19`
- All observed null values occur in election year `2024`
- No null `mode` values were observed from 2000–2020

Several labels appear semantically related but are not standardized to a
single vocabulary, including:

- `EARLY`, `EARLY VOTE`, `EARLY VOTING`
- `MAIL`, `MAIL-IN`, `ABSENTEE BY MAIL`
- `PROV`, `PROVISIONAL`

Normalization requirements should be determined during staging design rather
than applied to the raw source.

---

## Initial Type Considerations

These are observations for future staging design, not transformations applied
during raw-data inspection.

| Column | Raw Type | Likely Analytical Type | Reason |
|---|---|---|---|
| `county_fips` | `VARCHAR` | `VARCHAR` | Geographic identifier; leading zeros matter |
| `candidatevotes` | `VARCHAR` | `BIGINT` nullable | Semantically numeric; source contains `NA` |
| `version` | `BIGINT` | `DATE` | Encoded as `YYYYMMDD` |

No raw source values are modified during the discovery phase.