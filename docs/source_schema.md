# Source Schema

## MIT County Presidential Returns 2000-2024
    -File format: .csv

### Raw Columns

| Column | Source Description | Notes |
|---|---|---|
| `state` | State name | Raw source field |

| `county_name` | County name | Raw source field |

| `year` | Election year | Raw source field |

| `state_po` | State postal abbreviation | Raw source field |

| `county_fips` | County FIPS code | Raw source field |

| `office` | Office contested | Expected to be President |

| `candidate` | Candidate name | Raw source field |

| `party` | Candidate party | Raw source field |

| `candidatevotes` | Votes received by candidate | Raw source field |

| `totalvotes` | Total votes cast in county-year | Raw source field |

| `version` | Dataset finalization date/version | Raw source field |

| `mode` | Ballot mode | Usually `TOTAL`; varies for 2020 |




### DuckDB Inferred Types
- `county_fips` inferred as `BIGINT`; likely should be treated as a string identifier.
- `version` inferred as `BIGINT`; inspect raw values before deciding on final type.

### Type observations

- 'state'
    - Source meaning: State name
    - DuckDB type: `VARCHAR`
    - Null count: 0
    - Distinct count: 51
    - Format: Full uppercase state names
    - Observations:
        - Contains the 50 U.S. states plus the District of Columbia
        - No missing values observed
        - No obvious formatting inconsistencies observed
    



- 'county_name'
    - Source meaning: county name
    - DuckDB type: `VARCHAR`
    - Null count: 0
    - Distinct count: 1921
    - Observations:
        - No missing values observed
        - 1,921 unique county-name strings are present




- 'year'
    - Source meaning: State name
    - DuckDB type: `BIGINT`
    - Null count: 0
    - Distinct count: 7
    - Minimum: `2000`
    - Maximum: `2024`
    - Observed values:
    - `2000`
    - `2004`
    - `2008`
    - `2012`
    - `2016`
    - `2020`
    - `2024`
    - Observations:
        - Values follow the expected four-year presidential election cadence
        - No missing or unexpected years observed




- 'state_po'
    - Source meaning: U.S. postal abbreviation for the state
    - DuckDB type: `VARCHAR`
    - Null count: 0
    - Distinct count: 51
    - Format: Two-character uppercase postal abbreviations
    - Observations:
        - Includes the 50 states plus `DC`
        - No missing values observed
        - No obvious formatting inconsistencies observed



- 'county_fips'
    - Source meaning: County FIPS code
    - DuckDB type: `VARCHAR`
    - Null count: `0`
    - Literal `NA` count: `52`
    - Distinct count: `3,158`

    #### Observed lengths
    - 4 characters: `10,858` rows
    - 5 characters: `83,220` rows
    - 7 characters: `21` rows

    #### Observations
        - Standard county identifiers are expected to be 5 characters.
        - 4-character values appear consistent with county codes whose leading zero is not preserved.
        - The only observed 7-character value is `2938000`, which corresponds to the Census place GEOID for Kansas  City city, Missouri, not a county GEOID.
        - `NA` occurs on special non-county records such as `STATEWIDE WRITEIN`, `MAINE UOCAVA`, and `FEDERAL PRECINCT`.
        - These `NA` values should not automatically be treated as erroneous missing data.
        - The source codebook separately notes a special Alaska 2004 treatment for this field.




- 'office'
    - Source meaning: Office being contested
    - DuckDB type: `VARCHAR`
    - Null count: `0`
    - Distinct count: `1`
    - Observed value:
    - `US PRESIDENT`
    - Observations:
        - No missing values observed
        - No formatting variants observed
        - Column is constant across the dataset




- 'candidate'
    - Source meaning: Candidate name
    - DuckDB type: `VARCHAR`
    - Null count: `0`
    - Distinct count: `19`
    - Observations:
        - Most values are individual presidential candidates.
        - The field also contains non-candidate aggregate/status categories:
            - `OTHER`
            - `OVERVOTES`
            - `UNDERVOTES`
            - `SPOILED`
            - `TOTAL VOTES CAST`
        - Therefore, `candidate` is not strictly a person-name field in the raw source.
        - Downstream modeling may need to distinguish actual candidates from aggregate/status categories.
        - Contains two strings for 1 candidate: DONALD J TRUMP and DONALD TRUMP, may normalize later.




- 'party'
    - Source meaning: Candidate party
    - DuckDB type: `VARCHAR`
    - Null count: `501`
    - Distinct non-null count: `5`
    - Observed non-null values:
    - `DEMOCRAT`
    - `GREEN`
    - `LIBERTARIAN`
    - `OTHER`
    - `REPUBLICAN`

    #### Observations
        - Non-null values match the categories documented in the source codebook.
        - All 501 null values are associated with non-candidate/status records:
        - `TOTAL VOTES CAST`: 427
        - `UNDERVOTES`: 37
        - `OVERVOTES`: 23
        - `SPOILED`: 14
        - Null party values therefore appear semantically appropriate rather than missing candidate-party data.




- 'candidatevotes'
    - Source meaning: Votes received by the candidate/category for that party
    - DuckDB type: `VARCHAR`
    - Null count: `0`
    - Distinct count: `22,108`
    - Literal `NA` count: `37`
    - Other non-numeric count: `0`

    #### Observations
        - All non-`NA` values are numeric and can be cast to `BIGINT`.
        - The presence of `NA` causes DuckDB to infer the column as `VARCHAR`.
        - The field is semantically numeric and will likely require `NA` handling plus numeric casting downstream.




- 'totalvotes'
    - Source meaning: Total number of votes cast in the county-year
    - DuckDB type: `BIGINT`
    - Null count: `0`
    - Distinct count: `16,846`

    #### Observations
        - All observed values are numeric.
        - No missing values observed.
        - Values range from `0` upward into the millions.
        - No obvious type or formatting issues observed.




- 'version'
    - Source meaning: Date when the dataset was finalized
    - DuckDB type: `BIGINT`
    - Null count: `0`
    - Distinct count: `1`
    - Observed value:
    - `20260225`

    #### Observations
        - The value is stored as an 8-digit numeric value in `YYYYMMDD` format.
        - All rows contain the same version value.
        - Semantically represents a date rather than a numeric measure.
        - Will likely be parsed to a proper `DATE` type downstream.




- 'mode'
    - Source meaning: Mode of ballots cast
    - DuckDB type: `VARCHAR`
    - Null count: `2,795`
    - Distinct non-null count: `19`

    #### Observations
        - 19 distinct non-null ballot-mode labels are present.
        - All 2,795 null values occur in election year `2024`.
        - No null `mode` values were observed for 2000–2020.
        - Several labels appear semantically related but use different terminology, e.g.:
        - `EARLY`, `EARLY VOTE`, `EARLY VOTING`
        - `MAIL`, `MAIL-IN`, `ABSENTEE BY MAIL`
        - `PROV`, `PROVISIONAL`
        - Further investigation may be needed before deciding whether these labels should be normalized downstream.

















- `county_fips`
  - DuckDB inferred `BIGINT`
  - FIPS codes are 5-character identifiers
  - Leading zeros are not preserved when treated numerically
  - Should be cast to `VARCHAR` downstream

- `version`
  - DuckDB inferred `BIGINT`
  - Raw values use `YYYYMMDD` format, e.g. `20260225`
  - Should be parsed to a proper `DATE` downstream

 - `candidatevotes`
  - DuckDB inferred `VARCHAR`
  - 37 rows contain the string `NA`
  - Observed in 2024 New Mexico records for the Libertarian candidate
  - Further inspection required to determine whether these represent
    missing county totals, ballot-mode records, or another source-specific convention