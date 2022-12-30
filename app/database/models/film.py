"""Model that defines a film"""
from typing import List, Dict, Union, TypedDict
from bson import ObjectId
from .location import Location


class FilmDict(TypedDict):
    id: ObjectId
    name: str
    tags: List[str]
    categories: List[str]
    file_location: Location
    thumbnail_location: Location
    description: str
    tag_line: str


class Film:
    id: ObjectId
    name: str
    tags: List[str]
    categories: List[str]
    file_location: Location
    thumbnail_location: Location
    description: str
    tag_line: str

    def __init__(self, id: str, name: str, tags: List[str], categories: List[str], file_location: Location,
                 thumbnail_location: Location, description: str, tag_line: str):
        self.id = id
        self.name = name
        self.tags = tags
        self.categories = categories
        self.file_location = file_location
        self.thumbnail_location = thumbnail_location
        self.description = description
        self.tag_line = tag_line

    @property
    def dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "tags": self.tags,
            "categories": self.categories,
            "file_location": self.file_location.dict,
            "thumbnail_location": self.thumbnail_location.dict,
            "description": self.description,
            "tag_line": self.tag_line
        }

    @classmethod
    def from_dict(cls, data: dict):
        for field in ["_id", "name", "tags", "categories", "file_location", "thumbnail_location", "description",
                      "tag_line"]:
            if field not in data:
                raise ValueError(f"Field {field} missing")
        _file_location = Location.from_dict(data["file_location"])
        _thumbnail_location = Location.from_dict(data['thumbnail_location'])
        return cls(data["_id"], data["name"], data["tags"], data["categories"], _file_location, _thumbnail_location,
                   data["description"], data["tag_line"])
