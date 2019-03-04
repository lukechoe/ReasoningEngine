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

        b1 = self.kb.ask("(ON ?X TABLE)")
        b2 = self.kb.ask("(populationOfRegion ?Y ((UnitOfCountFn HomoSapiens) 6560608))")
        b3 = self.kb.ask("(relationAllInstance outerRadius AutomobileTire (?Z 0.5 0.9))")

        # expects honduras - Y....... meter - Z
        #b2 = self.kb.ask("(populationOfRegion Honduras ((UnitOfCountFn HomoSapiens) 6560608))")
        #b3 = self.kb.ask("(relationAllInstance outerRadius AutomobileTire (Meter 0.5 0.9))")

        #print(b1[0].var, '::' , b1[0].constant)
        #print(b2[0].var, '::' , b2[0].constant)
        #print(b3[0].var, '::' , b3[0].constant)



if __name__ == '__main__':
    unittest.main()
