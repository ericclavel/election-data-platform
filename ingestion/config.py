## Dataset Configurations

from dataclasses import dataclass
from pathlib import Path




@dataclass(frozen=True)
class DatasetConfig:
    source: str
    dataset: str
    dataset_doi: str
    file_prefix: str


    @property
    def raw_data_dir(self) -> Path:
        return Path("data/raw") / self.source / self.dataset

    @property
    def current_metadata_path(self) -> Path:
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
)

US_HOUSE = DatasetConfig(
    source="mit_election_lab",
    dataset="us_house",
    dataset_doi="doi:10.7910/DVN/IG0UN2",
    file_prefix="1976-2024-house",
)

US_SENATE = DatasetConfig(
    source="mit_election_lab",
    dataset="us_senate",
    dataset_doi="doi:10.7910/DVN/PEJ5QU",
    file_prefix="1976-2024-senate-state",
)


DATASETS = [
    COUNTY_PRESIDENTIAL,
    US_HOUSE,
    US_SENATE,
]