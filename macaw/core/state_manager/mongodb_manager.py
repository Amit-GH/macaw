from typing import Optional

import pymongo

from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult


class MongoDbManager:
    _db = pymongo.MongoClient().test  # TODO: add a dynamic way to change the db name

    @classmethod
    def _get_collection(cls, collection_name: str) -> Collection:
        """Returns the collection with the given collection name.

        Args:
            collection_name (str): The collection name in the database to retrieve.

        Returns:
            Collection: The collection to retrieve from the database
        """
        return cls._db[collection_name]

    @classmethod
    def query(cls, collection_name: str, filter: dict, limit: int) -> list:
        """Gets all documents in the given collection with the given filter.

        Args:
            collection_name (str): The name of the collection.
            filter (dict): The filtering criteria.

        Returns:
            list: The list of documents in the given collection that satisfy the criteria in the filter.
        """
        collection = cls._get_collection(collection_name)
        return collection.find(
            filter, limit=limit, sort=[("creation_time", pymongo.DESCENDING)]
        )

    @classmethod
    def put_document(cls, collection_name: str, document: dict) -> InsertOneResult:
        """Puts a document in the given collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to insert into the collection.

        Returns:
            InsertOneResult: The results of the one insert.
        """
        collection = cls._get_collection(collection_name)
        return collection.insert_one(document)

    @classmethod
    def update_document(
        cls, collection_name: str, filter: dict, update: dict
    ) -> Optional[UpdateResult]:
        """Updates the document found in the given collection by the given filter with the given updates.

        Args:
            collection_name (str): The name of the collection.
            filter (dict): The filtering criteria.
            update (dict): The updates to be made to the document found.

        Returns:
            Optional[UpdateResult]: The results of the update.
        """
        collection = cls._get_collection(collection_name)
        return collection.find_one_and_update(
            filter, update, sort=[("creation_time", pymongo.DESCENDING)]
        )
