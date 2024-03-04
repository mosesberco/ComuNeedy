import unittest
import main
from main import *

class TestMain(unittest.TestCase):
    def test_AddUser(self):
        new_person = User(First_name="moshe", Last_name="bercovici", Email="moses@meatmoses.com", Password="123456",
                    City="beer sheva", Age=25, Proficiency="doctor", Role="admin", Last_login=func.now())
        self.assertEquals()