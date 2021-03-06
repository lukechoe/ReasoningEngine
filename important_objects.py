class Fact(object):
    def __init__(self, data, label="IN"):
        super(Fact, self).__init__()
        self.id = "Fact"
        self.label = label
        self.predicate = data[0]
        self.terms = data[1:]

        self.antecedent = []
        self.consequent = []

    def __eq__(self, next):
        return self.predicate == next.predicate and self.terms == next.terms and isinstance(next, Fact)

    def __repr__(self):
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

        self.antecedent = []
        self.consequent = []

    def __eq__(self, next):
        return isinstance(next, Rule) and self.predicate == next.predicate and self.vars == next.vars and self.asserted == next.asserted
    def __repr__(self):
        s = "Rule: %s\n PRED: %s\n VARS: %s\n ASSERT: %s\n\n" % (self.label, self.predicate, self.vars, self.asserted)
        return s

# Justification is a pair of fact and rule that support another fact or rule
class Antecedent(object):
    def __init__(self, f, r):
        super(Antecedent, self).__init__()
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

# CLASS USED FOR SUGGESTIONS (like FIRE)
class Suggestion(object):
    def __init__(self, data):
        # assuming data is in 2D array format
        self.name = data[0][1]
        self.function = data[1]
        self.function_name = data[1][0]
        self.function_param = data[1][1:]
        self.tests = []
        self.subgoals = data[2]
        self.result_step = data[3][1:]
    def __repr__(self):
        s = "Suggestion:\n%s\n" % (self.name)
        return s

# The object that a user would give as input
class Question(object):
    def __init__(self, name, suggestion, question):
        self.name = name
        self.suggestion = suggestion
        self.suggestion_list = suggestion.replace('(', '')
        self.suggestion_list = suggestion.replace(')', '')
        self.suggestion_list = suggestion.split()
        self.question = question
    def __repr__(self):
        s = "Question:\n%s\n" % (self.name)
        return s
