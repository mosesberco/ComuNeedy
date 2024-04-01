import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
import main
from main import Base, User, SessionLocal, email_in_db, get_db,api_app


@pytest.fixture
def mock_db():
    mock_session = MagicMock(spec=Session)
    yield mock_session

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///test_users.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_email_in_db_exists(self):
        db = self.Session()
        # the follwoing 2 statements may need to be un-commented in first running of the file #
        # user = User(First_name="FirstName1", Last_name="LastName1", Email="udivak9@gmail.com", Password="password", Age=1, Address="Address1", City="City1", Last_login=func.now(), Proficiency="Beginner", Role="User", IsBlocked=False)
        # db.add(user)
        db.commit()

        self.assertTrue(main.email_in_db("user1@example.com", db))

    def test_email_in_db_not_exists(self):
        db = self.Session()

        self.assertFalse(main.email_in_db("nonexistent@example.com", db))


def test_add_user(mock_db):
    # Mock user data
    user_data = {
        "First_name": "John",
        "Last_name": "Doe",
        "Email": "john.doe@example.com",
        "Password": "mypassword",
        "City": "New York",
        "Age": 30,
        "Proficiency": "Expert",
        "Role": "Developer"
    }

    # Call the AddUser function with the mock data
    result = api_app.AddUser(user_data=user_data, db=mock_db)

    # Check if the function executed without any errors
    assert result is None

    # Check if the database session was used correctly
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # Check if the function extracted the correct user data
    assert user_data["First_name"] == "John"
    assert user_data["Last_name"] == "Doe"
    assert user_data["Email"] == "john.doe@example.com"
    assert user_data["Password"] == "mypassword"
    assert user_data["City"] == "New York"
    assert user_data["Age"] == 30
    assert user_data["Proficiency"] == "Expert"
    assert user_data["Role"] == "Developer"

    # Check if the Last_login was set correctly
    assert isinstance(user_data["Last_login"], datetime)





if __name__ == "__main__":
    unittest.main()