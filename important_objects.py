

class Fact(object):
    def __init__(self, data, justification=[], label="IN"):
        super(Fact, self).__init__()
        self.id = "Fact"
        self.label = label
        self.predicate = data[0]
        self.terms = data[1:]

        self.justification = justification
        self.supports = []

    def __eq__(self, next):
        return self.predicate == next.predicate and self.terms == next.terms and isinstance(next, Fact)

    def __repr__(self):
        #s = "Fact: %s\n %s\n\n %s\n" % (self.label, self.predicate, self.terms)
        lst = []
        for e in self.terms:
            lst.append(e)
        s = "Fact: \nPRED: %s \nTERMS: %s\n" % (self.predicate, str(lst))
        return s

class Rule(object):
    def __init__(self, data, asserted, back_support=[], label="IN"):
        super(Rule, self).__init__()
        self.id = "Rule"
        self.label = label

        # data is a 2D array, each list is a rule
        self.rule_list = data

        # rule: (<predicate> <vars> <vars>, <predicate> <vars> <vars> ==> <asserted>) in a list
        self.predicate = [item[0] for item in self.rule_list]
        self.vars = [item[1:] for item in self.rule_list]
        self.asserted = asserted

        self.back_support = back_support
        self.forward_support = []

    def __eq__(self, next):
        return self.predicate == next.predicate and self.vars == next.vars and self.asserted == next.asserted and isinstance(next, Rule)
    def __repr__(self):
        s = "Rule: %s\n PRED: %s\n VARS: %s\n ASSERT: %s\n\n" % (self.label, self.predicate, self.vars, self.asserted)
        return s

# Justification is a pair of fact and rule that support another fact or rule
class Justification(object):
    def __init__(self, f, r):
        super(Justification, self).__init__()
        self.fact = f
        self.rule = r

class Binding(object):
    def __init__(self, vars, constants):
        super(Binding, self).__init__()
        self.vars = vars
        self.constants = constants
    def __repr__(self):
        s = "Binding:\n %s\n%s\n\n" % (self.vars, self.constants)
        return s
