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

        b5 = self.kb.ask("(this_does_not_exist ?x ?y)")
        self.assertFalse(b5)


    """ MAY NOT NEED THIS ONE"""
    # This tests the functionality of reverse_ask()
    # this also returns bindings but the input is a fact rather than a rule
    def test04(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/data.txt'
        data = tokenize_file(file)

        classify(self.kb, data)
        b1 = self.kb.reverse_ask("(ON D TABLE)")
        #self.assertEqual(b1[0].vars[0], "?X")
        #self.assertEqual(b1[0].constants[0], "D")


    # This tests to see if the proper inferences were able to be made given a fact
    def test05(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/inferences.txt'
        data = tokenize_file(file)
        classify(self.kb, data)

        expected1 = Fact(['isa', 'luke', 'mortal'])
        expected2 = Fact(['happy', 'luke'])
        expected3 = Fact(['perfect', 'luke'])

        check = False
        if expected1 in self.kb.facts and expected2 in self.kb.facts and expected3 in self.kb.facts:
            check = True
        self.assertTrue(check)

        check = False
        expected1 = Fact(['above', 'block1', 'block3'])
        expected2 = Rule([['above', 'block2', '?z']], ['above', 'block1', '?z'])
        expected3 = Rule([['above', 'block3', '?z']], ['above', 'block2', '?z'])
        if expected1 in self.kb.facts and expected2 in self.kb.rules and expected3 in self.kb.rules:
            check = True
        self.assertTrue(check)


        """ Add additional facts and rules to knowledgebase"""
        check = False
        self.kb.add(Fact(['isa', 'dave', 'human']))
        expected1 = Fact(['isa', 'dave', 'mortal'])
        expected2 = Fact(['happy', 'dave'])
        expected3 = Fact(['perfect', 'dave'])
        #print(expected1)
        if expected1 in self.kb.facts and expected2 in self.kb.facts and expected3 in self.kb.facts:
            check = True
        self.assertEqual(check, True)


        #for e in self.kb.rules:
            #print(e)


if __name__ == '__main__':
    unittest.main()
