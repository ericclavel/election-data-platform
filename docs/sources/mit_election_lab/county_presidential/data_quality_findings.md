# Data Quality Findings

## Summary

Raw-source inspection identified several data-quality and standardization issues that affect interpretation of the county presidential dataset.

The most significant finding is that the apparent row grain is not universally unique. The proposed natural key uniquely identifies records from `2000–2020`, but collisions occur in `2024`.

The 2024 collisions are limited to:

* North Carolina
* South Carolina
* California
* Arizona
* Connecticut

Investigation shows that these collisions do not represent one uniform duplicate-row problem. They result from several distinct source-standardization and aggregation behaviors documented below.

Additional schema-level observations, including null handling, identifier formats, and inferred column types, are documented in [Source Schema](./source_schema.md).

## Duplicate / Repeated Rows

### Expected Grain

One row is expected to represent one candidate or vote category within a combination of:

* election year
* state
* county/reporting geography
* office
* party
* ballot/reporting mode

The proposed grain was tested using:

* `year`
* `state_po`
* `county_name`
* `county_fips`
* `office`
* `candidate`
* `party`
* `mode`

### Validation Result

The proposed grain is unique for election years `2000–2020`.

All observed grain collisions occur in `2024`.

| State     | Non-unique groups | Physical rows | Max rows/group |
| --------- | ----------------: | ------------: | -------------: |
| NC        |               300 |         1,200 |              4 |
| SC        |               138 |           276 |              2 |
| CA        |                 8 |            16 |              2 |
| AZ        |                 8 |            16 |              2 |
| CT        |                 7 |            14 |              2 |
| **Total** |           **461** |     **1,522** |          **4** |

Because multiple distinct data-quality patterns are present, each affected state is investigated separately below.

## Geographic / Source-Standardization Issues

### North Carolina — 2024 Missing Mode Detail

#### Observed

All 1,300 North Carolina 2024 records have:

```text
mode = NULL
```

Candidate row counts are:

| Candidate       | Rows | Counties | Rows/county |
| --------------- | ---: | -------: | ----------: |
| Chase Oliver    |  400 |      100 |           4 |
| Donald J Trump  |  400 |      100 |           4 |
| Kamala D Harris |  400 |      100 |           4 |
| Other           |  100 |      100 |           1 |

The three named candidates therefore contain four physical rows per county despite `mode` being null.

Example:

North Carolina / Alleghany / Donald J Trump contains four rows with different `candidatevotes`:

* `125`
* `11`
* `1053`
* `3711`

#### Interpretation

The source retains multiple vote-count observations for each named candidate but does not preserve the field required to distinguish those observations.

The semantic grain of these North Carolina records therefore cannot be fully reconstructed from the standardized dataset alone.

#### Status

Root cause substantially characterized.

The exact mapping of the four rows to upstream reporting categories remains unresolved within the standardized dataset.

---

### South Carolina — 2024 Mode Collision

#### Observed

South Carolina contains 138 non-unique grain groups.

All occur where:

```text
mode = 'FAILSAFE PROVISIONAL'
```

The groups divide into two patterns:

| Pattern                               | Groups |
| ------------------------------------- | -----: |
| Two different `candidatevotes` values |     78 |
| Same `candidatevotes` value           |     60 |

`totalvotes` and `version` remain identical within all affected groups.

#### Interpretation

Multiple source observations appear under the same standardized `FAILSAFE PROVISIONAL` mode.

Some pairs retain different vote counts, while others become physically identical after standardization.

These records should therefore not automatically be treated as ordinary duplicate rows.

#### Status

Collision characterized.

The exact upstream transformation remains unresolved.

---

### California — 2024 Candidate Normalization Collision

#### Observed

California contains eight non-unique grain groups.

All affected records have:

```text
candidate = 'OTHER'
party = 'OTHER'
mode = 'TOTAL'
```

Each group contains two distinct `candidatevotes` values while `totalvotes` and `version` remain identical.

Affected counties:

* Sutter
* Tehama
* Trinity
* Tulare
* Tuolumne
* Ventura
* Yolo
* Yuba

#### Interpretation

Multiple upstream candidate categories have been collapsed into the same standardized:

```text
candidate = 'OTHER'
party = 'OTHER'
```

representation.

The standardized candidate fields therefore cannot uniquely identify the underlying source observations.

#### Status

Root cause identified as a candidate/category normalization collision.

---

### Arizona — 2024 Category Normalization Collision

#### Observed

Arizona contains eight non-unique grain groups involving 16 rows.

All affected records have:

```text
candidate = 'UNDERVOTES'
party = 'OTHER'
```

Affected counties:

* Coconino
* Pima

Affected modes:

* `TOTAL`
* `EARLY VOTING`
* `ELECTION DAY`
* `PROVISIONAL`

#### Pima County

Two distinct source categories appear under the standardized `UNDERVOTES` category.

This produces two rows for each affected mode.

#### Coconino County

Coconino shows the same apparent standardized-category collision, but the second set of values has not been fully reconciled to the upstream source.

#### Status

Pima root cause identified.

Coconino remains partially unresolved.

---

### Connecticut — 2024 Candidate Aggregation Inconsistency

#### Observed

Connecticut contains seven non-unique grain groups involving 14 rows.

All affected records have:

```text
candidate = 'OTHER'
party = 'OTHER'
mode = 'TOTAL'
```

The collisions occur in every Connecticut county except Fairfield.

#### Interpretation

Comparison against Connecticut's official 2024 Statement of Vote showed that multiple upstream candidate and write-in categories are represented under the standardized `OTHER / OTHER` classification.

In seven counties, Ayyadurai/Ellis write-in votes appear as a separate `OTHER` row while the remaining non-retained candidates/write-ins are aggregated into another `OTHER` row.

This creates two rows with identical standardized identifying fields.

Fairfield is handled differently. Its single `OTHER` value of `5,256` equals the combined total of Stein/Ware, Kennedy/Shanahan, and all official write-in votes, including Ayyadurai/Ellis.

#### Interpretation

Candidate aggregation is inconsistent across Connecticut counties in the 2024 standardized data.

The standardized `candidate` and `party` fields therefore cannot uniquely identify the underlying source observations for seven counties.

#### Status

Root cause characterized as inconsistent candidate/category aggregation during standardization.

## Candidate Key Assessment

### Proposed Natural Key

The following combination was tested as a likely natural key:

* `year`
* `state_po`
* `county_fips`
* `office`
* `candidate`
* `party`
* `mode`

### Result

The combination uniquely identifies records for election years `2000–2020`.

It does not uniquely identify all `2024` records.

The 2024 failures correspond to the documented source-standardization issues in:

* North Carolina
* South Carolina
* California
* Arizona
* Connecticut

### Conclusion

The raw dataset does not provide a universally reliable natural key.

A surrogate key may eventually be required downstream to uniquely identify physical rows, but a surrogate key would not resolve the underlying semantic grain ambiguity present in some 2024 source records.

## Findings Requiring Downstream Handling

The following findings may affect future staging and modeling decisions:

* Raw rows should not be deduplicated solely because their apparent natural-key fields match.
* `2024` records require special consideration because multiple source-standardization patterns can create grain collisions.
* Candidate/category normalization can collapse distinct upstream observations into identical standardized labels.
* Missing `mode` information can make the semantic grain of some records impossible to reconstruct from the standardized source alone.
* A downstream surrogate key may uniquely identify physical rows but should not be interpreted as resolving source-level semantic ambiguity.
* Raw source records should remain unchanged so that downstream transformations can be traced back to the original standardized dataset.

## Open Questions

* Can the four North Carolina vote observations per named candidate be reliably mapped back to upstream reporting modes?
* What upstream transformation produced the duplicated South Carolina `FAILSAFE PROVISIONAL` records?
* Can the unresolved Coconino `UNDERVOTES` observations be reconciled against the upstream Arizona source?
* Should downstream analytical models preserve ambiguous physical rows individually or introduce explicit source-quality classifications?
* What canonical grain should the platform use once multiple election datasets are compared?

These questions should be revisited during staging and cross-dataset schema design rather than resolved through modification of the raw source.
