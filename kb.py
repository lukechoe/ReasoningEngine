from important_objects import *
from util import *

class KnowledgeBase(object):

    def __init__(self):
        self.facts = []
        self.rules = []

    def __repr__(self):
        return 'KnowledgeBase {!r}, {!r}'.format(self.facts, self.rules)

    # returns list of bindings if there exists match(es)
    # input statement format is (on ?X table)
    def ask(self, statement):
        binding_lst = []

        
        return binding_lst

    # add and infer new facts/rules
    def add(self, statement):
        if isinstance(statement, Fact):
            # check for duplicates
            if statement in self.facts:
                print("Already asserted (fact)")
                return False
            self.make_inferences(statement)
            self.facts.append(statement)
        if isinstance(statement, Rule):
            if statement in self.rules:
                print("Already asserted (rule)")
                return False
            self.make_inferences(statement)
            self.rules.append(statement)

    # use "in" and "out"
    def make_inferences(self, statement):
        # list of bindings below..
        bindings = []
        if isinstance(statement, Fact):
            for rule in self.rules:
                bindings = find_bindings(self, statement, rule)
        elif isinstance(statement, Rule):
            for fact in self.facts:
                bindings = find_bindings(self, fact, statement)
        else:
            print("incorrect input type (make_inferences)")
            return False




    def make_retractions(self, statement):
        pass
