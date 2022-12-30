"""Location Object"""
from enum import Enum
from typing import Dict


class LocationProviders(Enum):
    AWS = "AWS"
    BB = "BB"  # Backblaze
    DO = "DO"  # Digital Ocean


class Location:
    """
    Defines a location of a files
    """
    provider: LocationProviders
    region: str
    file_path: str

    def __init__(self, provider: LocationProviders, region: str, file_path: str):
        self.provider = provider
        self.region = region
        self.file_path = file_path

    @property
    def dict(self) -> dict:
        """Return class as dict"""
        return {
            "provider": self.provider.value,
            "region": self.region,
            "file_path": self.file_path
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        if ("provider" not in data) or ("region" not in data) or ("file_path" not in data):
            raise ValueError("Missing value needed for Location")
        return cls(LocationProviders[data["provider"]], data["region"], data["file_path"])
