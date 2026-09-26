# Data Quality Findings

## Summary

The U.S. Senate source contains `3,945` rows covering election records from 1976 through 2024.

The file is internally consistent in several important ways:

* no exact duplicate rows were observed
* candidate vote values do not exceed reported total vote values
* vote counts contain no fractional values
* within every working event grouping, `SUM(candidatevotes) = totalvotes`
* state identifiers map consistently to one value per state

The main data-quality concerns are not basic corruption or missing numeric data. They are primarily **semantic and representational**:

* historical inconsistency in election-stage labels
* casing changes in categorical fields
* ambiguous unnamed write-in rows
* inconsistent party labeling
* inconsistent version formatting
* lack of a universally reliable natural event or row key
* at least one case where multiple real-world election rounds are combined under the same source event descriptors

Raw ingestion should preserve these source characteristics rather than silently correcting them.

## Missing Values

### `candidate`

`candidate` contains `423` null rows.

All 423 rows:

* have `writein = true`
* also have `party_detailed = NULL`

These rows represent unnamed/generic write-in result lines rather than ordinary missing candidate data.

An additional 49 write-in rows contain a populated candidate value, so `writein = true` does not imply `candidate IS NULL`.

### `party_detailed`

`party_detailed` contains `627` null rows.

The nulls are not limited to one semantic condition. They include:

* unnamed write-in rows
* some named write-in rows
* non-candidate reporting categories
* some named candidates

A null `party_detailed` value should therefore not automatically be interpreted as unknown party affiliation.

### `party_simplified`

Only two rows contain `party_simplified = NULL`.

Both correspond to non-party reporting categories rather than normal candidate-party records.

### Other fields

No observed nulls were found in the profiled identifier, election-control, vote-count, unofficial, or version fields.

DuckDB still reports the CSV-derived columns as nullable because the file does not define database constraints.

## Duplicate / Repeated Rows

No completely identical rows were found.

```text
exact duplicate row groups: 0
```

However, repeated descriptive combinations occur.

The most common cases involve:

```text
candidate = NULL
party_detailed = NULL
writein = true
```

Multiple such lines can occur within the same working election event.

Across every observed repeated unnamed-write-in group, each row has a distinct `candidatevotes` value. The rows are therefore distinct source records even though the available descriptive fields do not identify who or what each individual line represents.

A second form of repetition occurs in Louisiana 2002, where two named candidates each appear twice with different vote totals under otherwise identical event descriptors.

## Identifier Issues

A useful working election-event grouping is:

```text
year
+ state
+ stage
+ special
```

This creates `862` groups and generally groups the source records coherently.

It is not universally unique at the real-world election-round level.

Likewise, no stable descriptive natural key has been identified for every source row.

The combination:

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

is unique in the current dataset.

However, `candidatevotes` is a measure rather than an identity attribute. Including it establishes technical uniqueness but does not make the combination an appropriate semantic primary key.

A downstream model should not assume that source-field uniqueness is equivalent to stable entity identity.

## Categorical / Sentinel Values

### Stage encoding

The `stage` field contains five raw values:

```text
gen
GEN
pre
runoff
GEN RUNOFF
```

The encoding varies historically.

Observed examples show that equivalent or closely related election stages can be represented differently across years.

In older Georgia records, `pre` may identify the preceding election round while `gen` is used for the later runoff result. More recent Georgia records use explicit values such as `runoff` and `GEN RUNOFF`.

Therefore:

* `stage = 'gen'` cannot universally be interpreted as the initial general-election round
* raw stage values should be retained
* normalization requires explicit downstream rules rather than simple casing changes

### Mode encoding

`mode` contains:

```text
total
TOTAL
```

`total` is used from 1976–2021 and `TOTAL` from 2022–2024.

This appears to be a source-format/casing change rather than two distinct reporting modes.

### Party labels

`party_detailed` contains 195 distinct non-null values.

The field mixes:

* major parties
* minor parties
* historical parties
* affiliation/status labels
* fusion or combined labels
* reporting-related labels

Semantically similar values may be encoded differently, including `DEMOCRAT` and `DEMOCRATIC`.

The field should not be normalized during raw ingestion.

### Version values

`version` contains four raw values and uses inconsistent date-like formats:

```text
YYYYMMDD
MM/DD/YY
```

The field can vary within the same election year and should be preserved as source metadata.

### Numeric sentinels

No negative or fractional vote-count sentinel values were observed in `candidatevotes` or `totalvotes`.

## Vote / Numeric Field Issues

### `candidatevotes`

* inferred type: `DOUBLE`
* null count: `0`
* range: `1–9,036,252`
* fractional values: `0`

### `totalvotes`

* inferred type: `DOUBLE`
* null count: `0`
* range: `1–15,348,846`
* fractional values: `0`

Both fields behave as whole-number counts despite being inferred as floating-point values.

No row has:

```text
candidatevotes > totalvotes
```

Within every working event group:

```text
SUM(candidatevotes) = totalvotes
```

The vote arithmetic is therefore internally consistent under the source grouping.

However, arithmetic consistency does **not** prove that the grouping corresponds to exactly one real-world election round. Louisiana 2002 demonstrates that multiple rounds can be combined under the same event descriptors while the arithmetic still balances.

## Geographic / Source-Standardization Issues

The source covers all 50 states and does not include D.C.

The following identifier fields map consistently one-to-one with state in the current dataset:

* `state_po`
* `state_fips`
* `state_cen`
* `state_ic`

`state_cen` is inferred as `DOUBLE`, although all observed values are integer-valued.

These fields should be treated as identifiers rather than measures.

Any downstream conversion to standardized string representations or external geographic keys should occur outside the raw ingestion layer.

## Election-Specific Edge Cases

### Louisiana 2002

Louisiana 2002 contains multiple election rounds that cannot be distinguished using the available event fields.

Mary L. Landrieu appears twice:

```text
573347
638654
```

Suzanne Haik Terrell appears twice:

```text
339506
596642
```

All four rows share:

```text
year = 2002
state = LOUISIANA
stage = gen
special = false
mode = total
version = 20210114
```

The source therefore does not provide an event field that distinguishes the two rounds.

The source's `totalvotes` value for this grouping is `2,481,629`, and:

```text
SUM(candidatevotes) = totalvotes
```

This means the vote lines from both rounds are arithmetically combined within the source-defined event grouping.

As a result:

```text
year + state + stage + special
```

should be treated as a **working grouping key**, not a universally valid real-world election-event identifier.

### Georgia stage conventions

Georgia provides examples of changing stage conventions:

* `pre` appears in 1992 and 2008
* `runoff` appears in 2021
* `GEN RUNOFF` appears in 2022

Older records may use `gen` for a runoff while `pre` represents the preceding round.

Stage interpretation therefore requires historical/source-specific logic.

### Regular and special contests in the same grouping dimensions

There are 18 year/state/stage combinations containing both:

```text
special = false
special = true
```

Therefore `special` is not redundant and must be retained when identifying election-event groups.

### Unnamed write-ins

Unnamed write-in rows have:

```text
candidate = NULL
party_detailed = NULL
writein = true
```

Multiple such rows can occur within a single working event.

For every observed repeated group, the rows have different `candidatevotes` values.

The source therefore distinguishes them as separate result lines but does not provide descriptive candidate-level identity for those lines.

## Findings Requiring Downstream Handling

Downstream staging/modeling should account for the following:

1. Preserve raw `stage`, `mode`, party, version, and identifier fields before normalization.
2. Do not assume `stage = 'gen'` always represents the same conceptual election stage.
3. Retain `special` when constructing election-event groupings.
4. Do not treat `candidate` as a guaranteed person identifier.
5. Do not interpret `candidate IS NULL` as ordinary missing data when `writein = true`.
6. Keep `party_detailed` and `party_simplified` as separate concepts.
7. Do not derive a natural primary key merely by adding `candidatevotes`.
8. Consider a generated/surrogate row identifier downstream if stable row-level identity is needed.
9. Treat `year + state + stage + special` as a working source grouping rather than a guaranteed unique real-world election event.
10. Preserve enough raw lineage to revisit edge cases such as Louisiana 2002 after additional source documentation is inspected.
11. Cast or model vote counts as whole-number measures downstream if appropriate, while preserving the raw source values in the ingestion layer.
12. Keep source-format normalization separate from raw ingestion.

## Open Questions

* Does the MEDSL codebook provide a more precise definition of `stage`, particularly for historical Louisiana and Georgia election rounds?
* Does the accompanying Senate sources file contain information that could distinguish multiple rounds such as Louisiana 2002?
* Is there a documented semantic definition for the row-level `version` field?
* Is the 2022 shift from lowercase to uppercase `stage` and `mode` values the result of a source-system or methodology change?
* Can a stable election-event identifier be constructed once this Senate source is compared with House and presidential source structures?
* Should downstream staging introduce standardized election-stage concepts while retaining the original source stage alongside them?
* What surrogate-key strategy should be used for result lines that have no stable descriptive natural key?


## Source codebook freshness:
- Current Dataverse codebook asset is labeled for 1976–2024,
  but its contents still describe U.S. Senate returns through 2018.
- Several documented categorical conventions do not match values
  observed in the current 1976–2024 data.
- Source codebooks should therefore be preserved and version-tracked,
  but should not be assumed to fully describe the current data without
  empirical validation.


  Senate sources reference file:
- source-provided provenance/reference artifact
- appears focused on 2020 Senate result acquisition
- records state-level source URLs, certification/status notes,
  free-text data-quality notes, and missing-vote indicators
- categorical values are not standardized
- should be preserved raw and version-tracked independently