import pymongo.errors
import pytest
from unittest.mock import patch
import json
from src.util.dao import DAO
from dotenv import dotenv_values
import pymongo
import os

@pytest.fixture
def sut():
    base_dir = os.path.dirname(__file__)
    file = os.path.join(base_dir, 'validator_test.json')
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    dbUrl = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

    with open(file, 'r') as f:
        validator = json.load(f)

    with patch('src.util.dao.getValidator') as mockedValidator, \
        patch('src.util.dao.os.environ.get') as mockedEnvURL:

        mockedValidator.return_value = validator
        mockedEnvURL.return_value = dbUrl

        sut = DAO("test")

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
        assert "_id" in validation_result and data.items() <= validation_result.items()

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
        entryData = {
            "todo": "Fix the tv",
            "done": False,
        }

        sut.create(entryData)

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)
