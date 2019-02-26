

class Fact(object):
    def __init__(self, data, back_support=[], label="TRUE"):
        super(Fact, self).__init__()
        self.id = "Fact"
        self.label = label
        self.predicate = data[0]
        self.terms = data[1:]

        self.back_support = back_support
        self.forward_support = []

    def __eq__(self, next):
        return self.predicate == next.predicate and self.terms == next.terms and isinstance(next, Fact)

    def __repr__(self):
        #s = "Fact: %s\n %s\n\n %s\n" % (self.label, self.predicate, self.terms)
        s = "Fact: %s %s\n" % (self.predicate, self.terms[0])
        return s

class Rule(object):
    def __init__(self, predicate, vars, asserteded, back_support=[], label="TRUE"):
        super(Rule, self).__init__()
        self.id = "Rule"
        self.label = label

        # rule: (<predicate> <vars> <vars>, <predicate> <vars> <vars> ==> <asserted>)
        self.predicate = predicate
        self.vars = vars
        self.asserted = asserteded

        self.back_support = back_support
        self.forward_support = []

    def __eq__(self, next):
        return self.predicate == next.predicate and self.vars == next.vars and self.asserted == next.asserted and isinstance(next, Rule)
    def __repr__(self):
        s = "Rule: %s\n %s\n\n %s\n %s\n" % (self.label, self.predicate, self.vars, self.asserted)
        return s

# Duo is a pair of fact and rule that support another fact or rule
class Duo(object):
    def _init__(self, f, r):
        super(Duo, self).__init__()
        self.fact = f
        self.rule = r
