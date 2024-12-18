from pymongo import MongoClient
import os
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()


class MongoDBConnectionTest(unittest.TestCase):
    def setUp(self):
        # Load MongoDB URI from environment variable
        self.uri = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

        # Mock MongoClient
        self.client_patch = patch('pymongo.MongoClient')
        self.mock_client = self.client_patch.start()

        # Mock the database and collection
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()

        # Set up the mock behavior
        self.mock_client.return_value.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection


    def test_insert_document(self):
        # Test the behavior of inserting a document into the collection
        document = {"session_id": "123", "user_id": "456", "status": "active"}

        # Mock insert_one method
        self.mock_collection.insert_one.return_value = MagicMock(inserted_id="123")

        # Call insert_one to simulate inserting a document
        result = self.mock_collection.insert_one(document)

        # Assert insert_one was called with the correct document
        self.mock_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(result.inserted_id, "123")


if __name__ == '__main__':
    unittest.main()



