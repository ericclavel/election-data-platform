## Dataset Configurations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReferenceAsset:
    name: str
    match_field: str
    file_prefix: str

@dataclass(frozen=True)
class DatasetConfig:
    source: str
    dataset: str
    dataset_doi: str
    file_prefix: str
    reference_assets: tuple[ReferenceAsset, ...] = ()


    @property
    def raw_data_dir(self) -> Path:
        return Path("data/raw") / self.source / self.dataset

    @property
    def data_metadata_path(self) -> Path:
        return(
            Path("data/metadata")
            / self.source
            / self.dataset
            / "data.json"
        )




COUNTY_PRESIDENTIAL = DatasetConfig(
    source="mit_election_lab",
    dataset="county_presidential",
    dataset_doi="doi:10.7910/DVN/VOQCHQ",
    file_prefix="countypres_",
    reference_assets=(
        ReferenceAsset(
            name="codebook",
            match_field="label",
            file_prefix="County Presidential Returns",
        ),
        ReferenceAsset(
            name="sources",
            match_field="originalFileName",
            file_prefix="sources-president",
        ),
    )
)

US_HOUSE = DatasetConfig(
    source="mit_election_lab",
    dataset="us_house",
    dataset_doi="doi:10.7910/DVN/IG0UN2",
    file_prefix="1976-",
    reference_assets=(
        ReferenceAsset(
            name="codebook",
            match_field="label",
            file_prefix="codebook-us-house",
        ),
    )
)

US_SENATE = DatasetConfig(
    source="mit_election_lab",
    dataset="us_senate",
    dataset_doi="doi:10.7910/DVN/PEJ5QU",
    file_prefix="1976-",
    reference_assets=(
        ReferenceAsset(
            name="codebook",
            match_field="label",
            file_prefix="codebook-us-senate",
        ),
        ReferenceAsset(
            name="sources",
            match_field="originalFileName",
            file_prefix="sources-senate",
        ),
    ),
)


DATASETS = [
    COUNTY_PRESIDENTIAL,
    US_HOUSE,
    US_SENATE,
]