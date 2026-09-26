def validate_config

def build_metadata_url

def fetch_dataset_metadata

def load_current_metadata

def request_signed_url

def build_destination_path ---but will need to generalize the parameter name to something like 'base_dir' so primary ingestion passes config.raw_data_dir and reference sync passes config.reference_data_dir


def validate_download

def calculate_md5

def validate_checksum

def download_file

def calculate_sha256

def save_current_metadata

def configure_logging
















Very generic:
- calculate_sha256()
- calculate_md5()
- validate_checksum()
- validate_download()
- save_current_metadata()
- load_current_metadata()
- configure_logging()

Dataverse/shared-acquisition specific:
- request_signed_url()
- download_file()
- build_metadata_url()
- fetch_dataset_metadata()




