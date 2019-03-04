from important_objects import *
from parser import *
import unittest
from kb import *
from util import classify

class MyTests(unittest.TestCase):
    def test01(self):
        self.kb = KnowledgeBase()
        file = 'data.txt'
        data = tokenize_file(file)

        # takes in data from txt file and asserts and makes inferences
        classify(self.kb, data)

        







if __name__ == '__main__':
    unittest.main()
