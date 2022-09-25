import dataset
import unittest

class TestDataset(unittest.TestCase):

    def test_loading_dataset():
        dataset.load_dataset("C:\Users\sbues\VSCode\python\Machine_Learning\test\test_data")
        print("C:\Users\sbues\VSCode\python\Machine_Learning\\test\\test_data")
