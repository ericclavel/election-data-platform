# Data Sources

## MIT Election Data and Science Lab

### Dataset
County Presidential Election Returns, 2000–2024

### Source
Harvard Dataverse / MIT Election Data and Science Lab

### Purpose
Primary source for V1 county-level presidential election results.

### Access
- Accessed through Harvard Dataverse
- Dataset requires completion of a Dataverse guestbook
- Browser download succeeds after guestbook completion
- Direct API download was tested with a Dataverse API token
- Authenticated `GET /api/access/datafile/<file_id>` returned HTTP 400
- Automated acquisition may require handling the guestbook workflow through the Dataverse API

### Local Storage
Raw source files are stored in:

`data/raw/`

Raw files are treated as immutable and are not manually modified.

### Version / Retrieval
- Dataset version: 20.0
- Retrieved: 2026-09-08
- Dataverse file ID: 11723285

### Notes
The initial V1 workflow uses a manual browser download for discovery and schema inspection.

Automated ingestion is intentionally deferred until the source-access requirements are better understood.