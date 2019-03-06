from important_objects import *
from util import *
import re

class KnowledgeBase(object):

    def __init__(self):
        self.facts = []
        self.rules = []

    def __repr__(self):
        return 'KnowledgeBase {!r}, {!r}'.format(self.facts, self.rules)

    # returns LIST OF BINDINGS if there exists match(es) in FACTS ONLY
    # input statement format is e.g. (on ?X table) ==> returns (?X, Block1)
    def ask(self, statement):
        binding_lst = []

        statement = statement.strip().replace("(","").replace(")","")
        elements = statement.split()

        pred = elements[0]
        terms = elements[1:]

        for f in self.facts:
            lst_of_vars = []
            lst_of_const = []
            isComplete = True
            if f.predicate == pred and len(f.terms) == len(terms):
                num_of_vars = 0
                for i in range(len(f.terms)):
                    if terms[i][0] == '?':
                        num_of_vars += 1
                        lst_of_vars.append(terms[i])
                        lst_of_const.append(f.terms[i])
                    else:
                        if terms[i] != f.terms[i]:
                            isComplete = False
                #print(num_of_vars,'::', len(f.terms))
                if isComplete == True:
                    if len(lst_of_vars) != len(lst_of_const):
                        print("Error with bindings")
                        return False
                    num_of_bindings = len(lst_of_vars)/num_of_vars
                    for i in range(int(num_of_bindings)):
                        one_binding_vars = []
                        one_binding_const = []
                        for j in range(num_of_vars):
                            one_binding_vars.append(lst_of_vars[j])
                            one_binding_const.append(lst_of_const[j])
                        binding_lst.append(Binding(one_binding_vars, one_binding_const))
        if len(binding_lst) == 0:
            return False
        return binding_lst

    # this returns a LIST OF BINDINGS if there exists a fact that satisfies a FULL rule
    # Input: (on block1 table) ==> returns (?X, Block1) assuming there is the rule: (rule (on ?X table) (assert! ... ))
    def find_bindings_fact(self, statement):
        pass

    # add and infer new facts/rules ... uses "ask()" and "helper()"
    def add(self, statement):
        if isinstance(statement, Fact):
            # check for duplicates
            if statement in self.facts:
                print("Already asserted (fact)")
                return False

            self.facts.append(statement)
            for r in self.rules:
                #todo
                pass

        if isinstance(statement, Rule):
            if statement in self.rules:
                print("Already asserted (rule)")
                return False

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
