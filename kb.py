from important_objects import *
from util import *
import re
import copy
from copy import deepcopy

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

        if not isinstance(statement, list):
            statement = statement.strip().replace("(","").replace(")","")
            statement = statement.split()

        pred = statement[0]
        terms = statement[1:]
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


    # add and infer new facts/rules ... uses "ask()" and "helper()"
    def add(self, statement):
        if isinstance(statement, Fact):
            # check for duplicates
            if statement in self.facts:
                print("Already asserted (fact)")
                return False


            self.facts.append(statement)
            self.make_inferences(statement)

            for r in self.rules:
                #todo
                pass

        if isinstance(statement, Rule):
            if statement in self.rules:
                print("Already asserted (rule)")
                return False
            #self.make_inferences(statement)
            self.rules.append(statement)
            self.make_inferences(statement)


    # recursive function that is the bulk of the inferencing logic
    def make_inferences(self, statement):
        # list of bindings below..
        bindings = []
        if isinstance(statement, Fact):
            if statement in self.facts:
                pass
            for rule in self.rules:
                if len(rule.predicate) == 1 and rule.predicate[0] == statement.predicate:
                    b = self.find_bindings(statement, rule)
                    if b == False:
                        continue
                    new_assert = self.update_rest_of_rule(rule.asserted, b)

                    justification = Justification(statement, rule)
                    new_assert = Fact(new_assert)
                    new_assert.justification.append(justification)

                    statement.supports.append(new_assert)
                    rule.supports.append(new_assert)

                    self.facts.append(new_assert)
                    self.make_inferences(new_assert)


                elif len(rule.predicate) > 1 and rule.predicate[0] == statement.predicate:
                    b = self.find_bindings(statement, rule)
                    if b == False:
                        continue

                    # update rule then give it forward and backward supporting facts/rules
                    new_rule = self.update_rest_of_rule(rule, b)

                    justification = Justification(statement, rule)
                    new_rule.justification.append(justification)

                    statement.supports.append(new_rule)
                    rule.supports.append(new_rule)

                    self.rules.append(new_rule)
                    self.make_inferences(new_rule)
            return

        elif isinstance(statement, Rule):
            binding_lst = []

            """ logic for how to do rules:

            if there is one predicate and
            there is a match, then the "assert" can be added to the KB.

            if there is more than one, only check the very first and assert
            a new rule
            """

            check = False # if this is true by the end of the for loop, then we found a match
            for f in self.facts:
                if len(statement.predicate) == 1 and statement.predicate[0] == f.predicate:
                    b = self.find_bindings(f, statement)
                    if b == False:
                        continue

                    new_assert = self.update_rest_of_rule(statement.asserted, b)
                    justification = Justification(f, statement)
                    new_assert = Fact(new_assert)
                    new_assert.justification.append(justification)
                    self.facts.append(new_assert)
                    self.make_inferences(new_assert)

                elif len(statement.predicate) > 1 and statement.predicate[0] == f.predicate:
                    b = self.find_bindings(f, statement)
                    if b == False:
                        continue
                    new_rule = self.update_rest_of_rule(statement, b)
                    justification = Justification(f, statement)
                    new_rule.justification.append(justification)
                    self.rules.append(new_rule)
                    self.make_inferences(new_rule)
            return

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
        # this assumes the left hand side of a rule has more than one predicate
        # therefore, it takes the rest of the rule, and returns a new rule
        if isinstance(rest_of_rule, Rule):
            new_rule = deepcopy(rest_of_rule)
            #print(rest_of_rule)
            new_rule.predicate = new_rule.predicate[1:]
            new_rule.vars = new_rule.vars[1:]
            # do rest of left hand side
            for i in range(len(binding.vars)):
                for j in range(len(new_rule.vars)):
                    for k in range(len(new_rule.vars[j])):
                        if new_rule.vars[j][k] == binding.vars[i]:
                            new_rule.vars[j][k] = binding.constants[i]
            # do right hand side (assert)
                for j in range(len(rest_of_rule.asserted)):
                    if new_rule.asserted[j] == binding.vars[i]:
                        new_rule.asserted[j] = binding.constants[i]
            return new_rule
        # this assumes the left hand side of a rule has only one predicate. and returns a new fact
        else:
            # Soooo python defaults to pass by reference.. -_- ... this took forever
            new_rule = rest_of_rule.copy()
            for i in range(len(binding.vars)):
                for j in range(len(new_rule)):
                    if new_rule[j] == binding.vars[i]:
                        new_rule[j] = binding.constants[i]
        return new_rule
