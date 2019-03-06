from important_objects import *
from parser import *
import unittest
from kb import *
from util import classify

class MyTests(unittest.TestCase):

    # Tests to see if text file is correctly parsed
    def test01(self):
        self.kb = KnowledgeBase()
        file = "dataFiles/initial_test.txt"
        data = tokenize_file(file)

        self.assertEqual(data[0], ["isa", "luke", "human"])

        self.assertEqual(data[1][0], "on")
        self.assertEqual(data[1][1], "block1")
        self.assertEqual(data[1][2], "block2")

        self.assertEqual(data[2][0], "populationOfRegion")
        self.assertEqual(data[2][2], "UnitOfCountFn")
        self.assertEqual(data[2][4], "6560608")

        self.assertEqual(data[3][0], "rule")
        self.assertEqual(data[3][11], "?y")
        self.assertEqual(data[3][13], "'3-Tower")

        self.assertEqual(data[4][0], "rule")
        self.assertEqual(data[4][7], "testing")

    # Tests to see if the data that was parsed can be used to construct
    # instances of facts and rules
    def test02(self):
        self.kb = KnowledgeBase()
        file = "dataFiles/initial_test.txt"
        data = tokenize_file(file)
        classify(self.kb, data)
        self.assertTrue(isinstance(self.kb.facts[0], Fact))
        self.assertTrue(isinstance(self.kb.facts[1], Fact))
        self.assertTrue(isinstance(self.kb.facts[2], Fact))
        self.assertTrue(isinstance(self.kb.rules[0], Rule))
        self.assertTrue(isinstance(self.kb.rules[1], Rule))

        self.assertEqual(self.kb.facts[0].predicate, "isa")
        self.assertEqual(self.kb.facts[0].terms, ["luke", "human"])

        self.assertEqual(self.kb.rules[0].predicate[0], "on")
        self.assertEqual(self.kb.rules[0].vars[0], ["?x", "table"])
        self.assertEqual(self.kb.rules[0].predicate[1], "on")
        self.assertEqual(self.kb.rules[0].vars[1], ["?y", "?x"])
        self.assertEqual(self.kb.rules[0].asserted, ["3-Tower", "?x", "?y", "?z"])

    # Tests the functionality of kb.ask()
    # kb.ask() returns bindings for any matches
    def test03(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/data.txt'
        data = tokenize_file(file)

        classify(self.kb, data)

        b1 = self.kb.ask("(ON ?X TABLE)")
        b2 = self.kb.ask("(populationOfRegion ?Y ((UnitOfCountFn HomoSapiens) 6560608))")
        b3 = self.kb.ask("(relationAllInstance outerRadius AutomobileTire (?Z 0.5 0.9))")

        self.assertEqual(b1[0].vars[0], "?X")
        self.assertEqual(b1[0].constants[0], "D")

        self.assertEqual(b2[0].vars[0], "?Y")
        self.assertEqual(b2[0].constants[0], "Honduras")

        self.assertEqual(b3[0].vars[0], "?Z")
        self.assertEqual(b3[0].constants[0], "Meter")


        b4 = self.kb.ask("(ON ?first ?second)")

        self.assertEqual(b4[0].vars, ["?first", "?second"])
        self.assertEqual(b4[0].constants, ["D", "TABLE"])

        self.assertEqual(b4[1].vars, ["?first", "?second"])
        self.assertEqual(b4[1].constants, ["E", "D"])

        self.assertEqual(b4[2].vars, ["?first", "?second"])
        self.assertEqual(b4[2].constants, ["F", "E"])
        self.assertEqual(len(b4), 3)

    # This tests to see if the proper inferences were able to be made
    def test04(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/inferences.txt'
        data = tokenize_file(file)
        classify(self.kb, data)


if __name__ == '__main__':
    unittest.main()
