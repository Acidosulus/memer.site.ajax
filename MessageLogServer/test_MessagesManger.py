import pytest
from datetime import datetime, timedelta
from pymongo import MongoClient
from MessagesManager import MessageManager

@pytest.fixture(scope="module")
def test_manager():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["TestDB"]
    collection = db["TestCollection"]
    manager = MessageManager("mongodb://localhost:27017/", "TestDB", "TestCollection")
    yield manager
    client.drop_database("TestDB")

def test_save_message(test_manager):
    test_manager.save_message("test_user", "test_icon", "test_message", "test_hyperlink")
    saved_message = test_manager.db["TestCollection"].find_one({"username": "test_user"})
    assert saved_message is not None

def test_get_last_messages(test_manager):
    for i in range(5):
        test_manager.db["TestCollection"].insert_one({"username": "test_user", "dt": (datetime.now() - timedelta(minutes=i)),
                                        "icon": "test_icon", "message": f"test_message_{i}", "hyperlink": f"test_hyperlink_{i}"})
    last_messages = test_manager.get_last_messages("test_user", 3)
    assert len(last_messages) == 6

