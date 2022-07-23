import unittest 
from data import Data
import regression

class TestRegression(unittest.TestCase):
    
    def setUp(self) -> None:

        test_data = Data("test/test_data/test_set.csv","dep_feat", ",")
        self.reg1=regression.SingleVarRegression("feat1", test_data, "polynomial", 1)
        self.reg2=regression.SingleVarRegression("feat2", test_data, "polynomial", 1)
        self.reg3=regression.SingleVarRegression("feat3", test_data, "polynomial", 1)

        return super().setUp()

    def test_get_r_squard(self):
        self.assertEqual(self.reg1.get_r_squard(), 1)
        self.assertEqual(self.reg2.get_r_squard(), 1)
        self.assertEqual(self.reg3.get_r_squard(), 1)


if __name__ == "__main__":
    unittest.main()
        
