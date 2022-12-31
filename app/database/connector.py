"""Database Connector"""
from pymongo import MongoClient
from typing import Dict, Any, Union, Optional, List
from pymongo.collection import Collection
from bson import ObjectId
from .models.film import Film, FilmDict


class Connector:
    """
    Database connector for Film info
    """
    __uri: str
    __database: str
    _client: MongoClient[Dict[str, Any]]
    _Films: Collection[FilmDict]

    def __init__(self, uri: str, database: str):
        """
        Init
        :param uri: Connection URI
        :return: None
        """
        self.__uri = uri
        self.__database = database
        self._client = MongoClient(self.__uri)
        self._db = self._client[self.__database]
        self._Films = self._db.Films

    def get_film_by_id(self, film_id: Union[str, ObjectId]) -> Optional[Film]:
        """
        Get a film by ID
        :param film_id: film's ID
        :return: Film or None
        """
        if not isinstance(film_id, ObjectId):
            film_id = ObjectId(film_id)
        film = self._Films.find_one({"_id": film_id})
        if film:
            return Film.from_dict(film)

    def get_all_films(self) -> List[Film]:
        """
        Get films in a categories
        :return: List of Film(s)
        """
        films = self._Films.find({})
        return [Film.from_dict(x) for x in films]

    def get_category_films(self, category: str) -> List[Film]:
        """
        Get films in a categories
        :param category: name of string
        :return: List of Film(s)
        """
        films = self._Films.find({"categories": {"$in": [f"{category}"]}})
        return [Film.from_dict(x) for x in films]

    def get_tag_films(self, tag: str) -> List[Film]:
        """
        Get films with a tag
        :param tag: name of string
        :return: List of Film(s)
        """
        films = self._Films.find({"tags": {"$in": [f"{tag}"]}})
        return [Film.from_dict(x) for x in films]






