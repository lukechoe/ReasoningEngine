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
    def reverse_ask(self, statement):
        binding_lst = []

        statement = statement.strip().replace("(","").replace(")","")
        elements = statement.split()

        pred = elements[0]
        terms = elements[1:]


        #for r in self.rules:
            #for i in range(len(r.predicate)):
                # this is why i should've organized the objects...
                # now i gotta iterate through the list of predicates AND vars... -_-
                #if r.predicate[i] == pred:
                #    print(pred, '000')
            #print('break;')

    # add and infer new facts/rules ... uses "ask()" and "helper()"
    def add(self, statement):
        if isinstance(statement, Fact):
            # check for duplicates
            if statement in self.facts:
                print("Already asserted (fact)")
                return False

            #self.make_inferences(statement)
            self.facts.append(statement)

            for r in self.rules:
                #todo
                pass

        if isinstance(statement, Rule):
            if statement in self.rules:
                print("Already asserted (rule)")
                return False
            #self.make_inferences(statement)
            self.rules.append(statement)

    # given a fact, infer any new facts/rules
    def infer_with_fact(self, statement):

        for r in self.rules:
            for i in range(len(r.predicate)):
                # kb ask... right here.. translate rule into string format..
                # IMPORTANT somehow check to see if there are multiple results
                # that a "kb ask()" returns. Since there can be multiple bindings for ?X
                    print(r.predicate[i])


    # use "in" and "out"
    def make_inferences(self, statement):
        # list of bindings below..
        bindings = []
        if isinstance(statement, Fact):
            for rule in self.rules:
                if len(rule.predicate) == 1 and rule.predicate[0] == statement.predicate:
                    b = self.find_bindings(statement, rule)
                    if b == False:
                        continue
                    new_assert = self.update_rest_of_rule(rule.asserted, b)
                    justification = Justification(statement, rule)
                    new_assert = Fact(new_assert, justification)
                    self.add(new_assert)
                    self.make_inferences(new_assert)
                    # todo check back_support and implement forward support


                # more than one predicate...todo
                else:
                    pass
        elif isinstance(statement, Rule):
            for fact in self.facts:
                bindings = find_bindings(self, fact, statement)
        else:
            print("incorrect input type (make_inferences)")
            return False

    # returns a list of bindings for a given fact/rule pair. returns false if
    # there is no pattern matched
    def find_bindings(self, fact, rule):
        vars = []
        constants = []
        for i in range(len(rule.vars[0])):
            if rule.vars[0][i][0] == '?':
                vars.append(rule.vars[0][i])
                constants.append(fact.terms[i])
                #print(rule.vars[0][i], '---', fact.terms[i])
            else:
                if rule.vars[0][i] != fact.terms[i]:
                    return False
        return Binding(vars, constants)

    # takes the rest of a rule (could have more predicates and vars,
    # or it could just be the asserted)
    def update_rest_of_rule(self, rest_of_rule, binding):
        #print(len(binding.vars), '---')
        if isinstance(rest_of_rule, Rule):
            pass # todo this
        # this is just the asserted (hopefully)
        else:

            for i in range(len(binding.vars)):
                for j in range(len(rest_of_rule)):
                    if rest_of_rule[j] == binding.vars[i]:
                        rest_of_rule[j] = binding.constants[i]
        return rest_of_rule

    def make_retractions(self, statement):
        pass
