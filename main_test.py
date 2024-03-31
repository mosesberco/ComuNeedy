import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

import main
from main import Base, User, SessionLocal, email_in_db

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

if __name__ == "__main__":
    unittest.main()