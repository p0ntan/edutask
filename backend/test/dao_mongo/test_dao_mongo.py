import pymongo.errors
import pytest
import unittest.mock as mock
from unittest.mock import patch
import json
from src.util.dao import DAO
import pymongo

@pytest.fixture
def sut():
    with open('./test/dao_mongo/validator_test.json', 'r') as f:
        validator = json.load(f)

    with patch('src.util.dao.getValidator') as mockedValidator, \
        patch('src.util.dao.os.environ.get') as mockedEnvURL:

        dbUrl = "mongodb://localhost:27017"

        mockedValidator.return_value = validator
        mockedEnvURL.return_value = dbUrl

        data = {
            "todo": "Fix the tv",
            "done": False,
        }

        sut = DAO("test")

        client = pymongo.MongoClient(dbUrl)
        collection = client.edutask.test
        collection.insert_one(data)

        yield sut

        client = pymongo.MongoClient(dbUrl)
        collection = client.edutask.test
        collection.drop()

@pytest.mark.assignment_3
class TestCreateTodo:
    def test_create_valid_data(self, sut):
        data = {
            "todo": "Fix the wall",
            "done": True
        }

        validation_result = sut.create(data)
        assert validation_result.keys() == {"_id", "todo", "done"}  # TODO fix assertion
        # assert validation_result == {
        #     "_id": "",
        #     "todo": "Fix the wall",
        #     "done": True
        # }

    @pytest.mark.parametrize('data', [
        ({
            # Type constraint not fulfilled
            "todo": "Fix my car, need new brakes.",
            "done": 0
        }),
        ({
            # Required properties not present
            "done": False
        }),
        ({
            # Property value not unique
            "todo": "Fix the tv",
            "done": True
        }),
    ])
    def test_invalid_data(self, sut, data):
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)
