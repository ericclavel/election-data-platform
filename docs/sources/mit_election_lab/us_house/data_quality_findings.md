# U.S. House 1976–2024 — Data Quality Findings

## Summary

The inspected U.S. House source contains:

* `33,805` rows
* `20` columns
* election years from 1976–2024
* district-level U.S. House election returns
* no SQL `NULL` values
* no exact duplicate rows

The source is generally structurally consistent, but several important edge cases affect downstream interpretation:

* literal `NA` values are used instead of SQL nulls in some fields
* `runoff` cannot safely be auto-inferred as Boolean
* candidate and party fields contain source reporting categories rather than only normalized entities
* fusion voting creates legitimate multiple party-line rows for one candidate
* generic write-in representation can be ambiguous or lossy
* some result rows contain ballot categories such as `BLANK` and `VOID`
* `candidatevotes` and `totalvotes` contain sentinel values
* `totalvotes` cannot always be assumed to equal the sum of every result row
* ranked-choice and other election-specific cases require additional interpretation

## Duplicate / Repeated Rows

### Exact Duplicates

No exact duplicate records were found across all 20 source columns.

### Descriptive-Key Collisions

The following candidate-party descriptive combination was tested:

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

It produced `85` collision groups.

The collisions were isolated to generic write-in records:

```text
candidate = WRITEIN
party = NA
writein = TRUE
```

When `writein = FALSE` was tested separately, the descriptive combination produced `0` collisions.

### Example: 2008 Maryland District 4

Four rows shared identical descriptive values but had different vote totals:

```text
WRITEIN | NA | 28
WRITEIN | NA | 48
WRITEIN | NA | 75
WRITEIN | NA | 453
```

The only observed distinguishing field among these rows was `candidatevotes`.

Including `candidatevotes` removes the collision, but `candidatevotes` is a measure and should not be treated as part of a natural key solely to force uniqueness.

### Implication

There is no universally reliable descriptive natural key for every raw row.

For non-write-in records, candidate-party result-line fields behave uniquely.

Generic write-in reporting requires separate downstream handling or a surrogate row identifier.

## Identifier Issues

### Numeric State Codes

The following fields are stored numerically but are identifiers:

```text
state_fips
state_cen
state_ic
```

They should not be treated as quantitative measures.

### District

`district` is also an identifier despite being stored as an integer.

Observed values range from `0–53`.

`district = 0` represents at-large/statewide congressional representation.

Historical use of `0` appears in several states because House representation and apportionment change over time.

District numbers alone should not be treated as stable geographic entities across election years.

## Categorical / Sentinel Values

### `runoff`

The raw `runoff` field contains:

```text
FALSE    25,141
NA        8,656
TRUE          8
```

There are no SQL nulls.

`NA` is therefore a literal source value rather than a database null.

It is highly structured:

* only `GEN` rows
* observed from 2006–2018

DuckDB's automatic Boolean inference is unsafe because `NA` cannot be converted to Boolean.

The exact semantic meaning of `NA` should be confirmed before standardization.

### `party`

The field contains `500` distinct raw labels.

Examples include:

* `DEMOCRAT`
* `REPUBLICAN`
* `LIBERTARIAN`
* `INDEPENDENT`
* `CONSERVATIVE`
* `WORKING FAMILIES`
* `NA`
* `NONE`
* `NO PARTY`
* `NO PARTY AFFILIATION`
* `UNAFFILIATED`
* `WRITE-IN`

It also contains historical/local labels and spelling variation.

Literal `NA` occurs `4,094` times and is not SQL null.

Raw party values should be retained separately from any standardized party classification.

### `candidate`

The candidate field contains `16,975` distinct raw values.

It is not exclusively a person-name field.

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

Downstream candidate dimensions should not treat every raw `candidate` value as a person.

### `mode`

`mode` is constant:

```text
TOTAL
```

across all `33,805` rows.

### `version`

`version` is constant:

```text
20250910
```

The field has date-like `YYYYMMDD` semantics rather than numeric-measure semantics.

## Vote / Numeric Field Issues

### Negative Sentinel Values

#### `candidatevotes`

Minimum observed value:

```text
-1
```

It occurs in one row:

```text
2020 Florida District 25
candidatevotes = -1
totalvotes = -1
```

The value should not be interpreted as a literal negative vote count.

#### `totalvotes`

`totalvotes = -1` occurs in three observed rows:

```text
2020 Florida District 25
2024 Florida District 20
2024 Oklahoma District 3
```

These values behave as source sentinel values rather than real negative vote totals.

The exact MEDSL convention for `-1` remains to be confirmed.

### `totalvotes` Is Not Always Constant Within an Event

A test using:

```text
year
state
district
stage
runoff
special
```

found five election groups with multiple `totalvotes` values:

```text
2018 Georgia Districts 6, 8, 9, 12, 13
```

Each case followed the same pattern:

* named-candidate rows carried a total excluding write-in votes
* the generic `WRITEIN` row carried a total including its own write-in votes

Examples:

```text
GA-06:
named-candidate total = 317014
write-in votes        =     18
write-in row total    = 317032
```

```text
GA-08:
named-candidate total = 198152
write-in votes        =    564
write-in row total    = 198716
```

This should be treated as a source/reporting convention, not evidence of two different election events.

### Non-Candidate Rows May Be Excluded From `totalvotes`

#### 2024 New York

All 2024 New York House districts initially failed a simple:

```text
SUM(candidatevotes) = totalvotes
```

test.

Inspection showed that the source includes ballot/reporting categories such as:

```text
BLANK
VOID
SCATTERING
```

For New York District 1:

```text
SUM(all candidatevotes) = 430460
BLANK                    =  19984
VOID                     =    376
totalvotes               = 410100
```

Removing `BLANK` and `VOID` yields:

```text
410100
```

which exactly matches `totalvotes`.

The same exclusion rule resolved all inspected 2024 New York district mismatches.

`SCATTERING` remained included in the total.

#### 2024 Maine District 1

The source contains:

```text
BLANK = 14037
```

Candidate vote totals excluding `BLANK` sum exactly to:

```text
425530
```

which matches `totalvotes`.

Therefore, a raw sum across every `candidate` category is not a reliable general method for reconstructing contest turnout.

### Generic Write-In Normalization Can Be Lossy

Some contests contain official write-in activity that is not fully recoverable from the standardized generic `WRITEIN` rows.

Observed examples include:

#### 2002 Indiana District 2

MEDSL includes:

```text
WRITEIN | 6 votes
```

but the reported contest total exceeds the sum of MEDSL candidate rows by another `6` votes.

External official election records contain multiple separate write-in candidates in that contest.

#### 2012 Connecticut District 3

MEDSL includes:

```text
WRITEIN | 1 vote
```

but the reported total exceeds the row sum by another `1` vote.

#### 2016 Connecticut District 1

MEDSL includes:

```text
WRITEIN | 1 vote
```

but the reported total exceeds the row sum by another `1` vote.

These cases indicate that normalization to the generic `WRITEIN` label can remove candidate-level distinction and may also prevent `SUM(candidatevotes)` from reproducing `totalvotes`.

### 2018 Maine District 2

Observed MEDSL values:

```text
JARED F GOLDEN   139231
BRUCE POLIQUIN   136326

SUM(candidatevotes) = 275557
totalvotes          = 281371
```

The contest used ranked-choice voting.

The mismatch does not behave like an ordinary plurality-election aggregation issue.

The source appears to combine values associated with different ranked-choice tabulation states or stages.

This contest should be treated as an election-specific edge case and verified against the underlying Maine tabulation files before downstream analytical use.

## Geographic / Source-Standardization Issues

### File Extension Does Not Match Actual Delimiter

The source file is named:

```text
1976-2024-house.tab
```

and Dataverse metadata identifies it as tabular/tab-separated.

The downloaded original content is actually comma-delimited.

Explicit tab-delimited parsing causes the complete header to be read as one column.

Ingestion should inspect or auto-detect the actual delimiter instead of assuming delimiter from extension alone.

### State Coding Systems

The following state fields were internally clean in inspection:

```text
state
state_po
state_fips
state_cen
state_ic
```

Each contained 51 distinct mappings corresponding to the 50 states plus District of Columbia.

## Election-Specific Edge Cases

### Multiple Election Events Within One District-Year

`year + state + district` is not sufficient to identify an election event.

Example: 1996 Texas District 25 contains both:

```text
PRI + special = TRUE + runoff = FALSE
```

and:

```text
GEN + special = FALSE + runoff = TRUE
```

within the same year/state/district.

Election stage and election-status fields are therefore required when identifying an election event.

### Fusion / Cross-Endorsed Candidates

The same candidate may legitimately appear several times in the same election under different party labels.

Example: 2018 New York District 2 includes Peter T. King on five distinct party result lines.

Each line has its own `candidatevotes`.

The `fusion_ticket` field is row-level:

* the base party line may be `FALSE`
* additional fusion/cross-endorsed lines may be `TRUE`

A test of all multi-party, non-write-in candidates found that every such candidate had at least one associated row where:

```text
fusion_ticket = TRUE
```

Candidate-level vote analysis must therefore account for multiple party lines.

### `unofficial`

`unofficial = TRUE` occurs only in 39 rows:

```text
2018 North Carolina: 32
2018 West Virginia:   7
```

This concentration should be preserved as source metadata rather than silently normalized away.

## Findings Requiring Downstream Handling

Future staging/modeling should account for the following:

* Preserve raw source values before standardization.
* Read `runoff` as text during ingestion rather than trusting Boolean auto-inference.
* Keep literal `NA` distinct from SQL `NULL`.
* Do not model every `candidate` value as a person.
* Preserve raw `party` values alongside any normalized party classification.
* Do not assume one row equals one unique person/candidate.
* Aggregate fusion party lines when analysis requires candidate-level totals.
* Do not blindly sum all `candidatevotes` rows to reconstruct `totalvotes`.
* Define explicit treatment for `BLANK`, `VOID`, `SCATTERING`, `UNDERVOTES`, and other reporting categories.
* Treat generic write-in records as potentially lossy or ambiguous.
* Do not use `candidatevotes` as a natural-key component merely to force uniqueness.
* Treat `-1` vote values as unresolved source sentinels until their semantics are formally confirmed.
* Preserve ranked-choice contests for election-specific treatment rather than forcing plurality-election assumptions onto them.
* Use a surrogate key or deterministic row identifier if downstream models require guaranteed row identity.

## Open Questions

1. What is MEDSL's exact semantic definition of literal `NA` in `runoff`?
2. What is the documented meaning of `-1` in `candidatevotes` and `totalvotes`?
3. Why are some generic `WRITEIN` reporting lines preserved separately while others appear to be collapsed or omitted?
4. What exact ranked-choice tabulation stage do the 2018 Maine District 2 `candidatevotes` values represent?
5. Are `BLANK`, `VOID`, `SCATTERING`, and similar categories represented consistently across states and election years?
6. Should future standardized models classify non-person candidate values through a dedicated result-line/category field rather than overloading the candidate dimension?
7. Does the current source version provide any hidden/source-level identifier that distinguishes repeated generic write-in reporting lines?

## House codebook:
- current coverage matches the 1976–2024 dataset
- substantially more current than the Senate codebook
- documents at-large district coding and fusion-ticket behavior
- documents uncontested-race handling using candidatevotes = 1
- does not document observed -1 sentinel values
- contains some internal casing inconsistencies
- generally useful, but still requires empirical validation against the data