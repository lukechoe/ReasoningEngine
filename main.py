from important_objects import *
from parser import *
import unittest
from kb import *
from util import classify
from util import classify_suggestions
from suggestions import *

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



    # This tests for inference functionality and
    # justifications of each fact/rule
    def test04(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/inDepthFactsRules.txt'
        data = tokenize_file(file)

        classify(self.kb, data)

        # f1 was inferred from a fact and rule in the knowledge base
        f1 = Fact(['isa', 'D', 'bottomBlock'])
        shouldBeTrue = False
        if f1 in self.kb.facts:
            shouldBeTrue = True
            index = self.kb.facts.index(f1)
        self.assertTrue(shouldBeTrue)
        # check to see if the inferred fact (f1) has justifications
        actual_fact = self.kb.facts[index]
        j1 = actual_fact.justification[0].fact
        j2 = actual_fact.justification[0].rule
        shouldBeTrue = False
        f = Fact(['ON', 'D', 'TABLE'])
        r = Rule([['ON', '?x', 'TABLE']], ['isa', '?x', 'bottomBlock'])

        if f == j1 and r == j2:
            shouldBeTrue = True
        self.assertTrue(shouldBeTrue)

        # check to see if the justifications support the given fact (f1)
        support1 = j1.supports[1]
        support2 = j2.supports[0]
        shouldBeTrue = False
        #both support1 and support2 should point to the original inferred fact (ON D TABLE)
        if f1 == support1 and f1 == support2:
            shouldBeTrue = True
        self.assertTrue(shouldBeTrue)

        # Fact(['ON', 'D', 'TABLE']) also supports another fact/rule!
        # Since it satisfies the first part of the rule:
        # (rule (ON ?x TABLE)
        #  (rule (ON ?y ?x)
        #    (rule (ON ?z ?y) (assert! '(3-Tower ,?x ,?y ,?z)))))
        # it will assert a new rule with the appropriate new bindings set
        # expected:
        # (rule (ON ?y D)
        #   (rule (ON ?z ?y))
        #     (assert! '(3-Tower D ,?y ,?z)))
        support3 = j1.supports[0]
        r = Rule([['ON', '?y', 'D'], ['ON', '?z', '?y']], ['3-Tower', 'D', '?y', '?z'])


        # Inferred facts and rules can infer more facts and rules ...
        f1 = Fact(['thereIsOneBlockBetween', 'C', 'TABLE'])
        f2 = Fact(['thereIsOneBlockBetween', 'B', 'D'])
        f3 = Fact(['thereIsOneBlockBetween', 'A', 'C'])
        shouldBeTrue = False
        if f1 in self.kb.facts and f2 in self.kb.facts and f3 in self.kb.facts:
            shouldBeTrue = True
        self.assertTrue(shouldBeTrue)

        f4 = Fact(['thereAreThreeBlocksBetween', 'A', 'TABLE'])
        shouldBeTrue = False
        if f4 in self.kb.facts:
            shouldBeTrue = True
        self.assertTrue(shouldBeTrue)


    # More testing to see if the proper inferences were able to be made
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

    # This tests the functionality of suggestions! This is similar to the
    # suggestions that are written in Common Lisp through FIRE reasoning engine
    def test06(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/data_for_suggestions.txt'
        data = tokenize_file(file)
        classify(self.kb, data)

        self.sb = SuggestionBase(self.kb)
        file = "dataFiles/suggestions.txt"
        #ensure that the txt file has each subgoal on a separate line
        data = tokenize_suggestion_file(file)
        classify_suggestions(self.sb, data)

        original_suggestions = copy.deepcopy(self.sb)

        # This question is the first test. The suggestion fetches for its subgoals
        # if the subgoals are more suggestions. If not, it will fetch from facts.
        # Since there is a fact that satisfies this suggestion, the answer is returned
        q = Question('question0', 'humanPopulation ?p', "what is the human population?")
        ans = self.sb.evaluate(q)
        self.assertEqual(float(ans), 7000000000.0)


        # This question tests the overall functionality of "evaluate()"
        self.sb = original_suggestions # restore original version of sb
        q = Question('question1', 'CaloriesIn moon ?count', 'How many calories in object?')
        ans = self.sb.evaluate(q)
        ans = float(ans)

        # Checking the evaluation process...

        # "CaloriesIn" will call the subgoals "volumeOfObject" and "caloriesInCubicMeter"
        # "volumeOfObject" is another suggestion that retrieves a radius then evaluates
        # the volume of sphere formula: 4.187 * (r^3)
        # the result is then put into ?vol, hence ?vol is replaced with the actual value:
        eval1 = ['2.1943324029411e+19', 'TimesFn', '4.187', 'TimesFn', '?radius', '?radius', '?radius']
        self.assertEqual(self.sb.eval[0], eval1)

        # Once "volumeOfObject moon ?vol" -> ?vol = 2.1943324029411e+19,
        # the next subgoal is checked. "caloriesInCubicMeter" is next.
        # this is another defined suggestion in the "suggestions.txt" file.
        # This suggestion has its own subgoals:
        # 1. (madeOf ?obj greencheese) - this will return (?obj = moon)
        # 2. (caloriesPerKilogram greencheese ?cpk) - this will search for a suggestion
        # named "caloriesPerKilogram". Since none is found, it will then search
        # facts (from data_for_suggestions.txt)
        # in the knowledgebase to "ask()" if a fact exists that matches the description.
        # This succeeds and returns (?cpk = 4000)
        # Then it evaluates the next subgoal, "densityOfGreenCheese" which will
        # go through the same logic as the previous subgoal. It will return (?dc = 947)
        # The suggestion multiplies ?cpk and ?dc -> 4000 * 947 = 3788000.
        eval2 = ['3788000.0', 'TimesFn', '?cpk', '?dc']
        self.assertEqual(self.sb.eval[1], eval2)

        # Now that all of the "CaloriesIn" subgoals have been evaluated,
        # with ?vol = 2.19...e+19 and ?cal = 3788000, we can move on to its
        # result-step. According to the the suggestions txt file, ?vol and ?cal
        # get multiplied to return the final ?count. 2.19e+19 * 3788000 =
        # 8.31e+25
        eval3 = ['8.312131142340886e+25', 'TimesFn', '2.1943324029411e+19', '3788000.0']
        self.assertEqual(self.sb.eval[2], eval3)

        # double checking to make sure the answer is roughly equivalent to
        # the answer given from FIRE reasoning engine.
        withinRange = False
        if ans > 1e25 and ans < 1e26:
            withinRange = True
        self.assertTrue(withinRange)


    # in depth suggestion unit test (calls multiple suggestions with recursive stack)
    def test07(self):
        self.kb = KnowledgeBase()
        file = 'dataFiles/data_for_suggestions.txt'
        data = tokenize_file(file)
        classify(self.kb, data)

        self.sb = SuggestionBase(self.kb)
        file = "dataFiles/suggestions.txt"
        #ensure that the txt file has each subgoal on a separate line
        data = tokenize_suggestion_file(file)
        classify_suggestions(self.sb, data)

        q = Question('question2', 'DurationFeedHumans moon ?time', "How long can the moon feed humans if it was made of green cheese?")
        ans = self.sb.evaluate(q)
        ans = float(ans)
        withinRange = False
        if ans > 1e12 and ans < 1e13:
            withinRange = True
        self.assertTrue(withinRange)

if __name__ == '__main__':
    unittest.main()
