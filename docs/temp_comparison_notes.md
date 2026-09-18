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