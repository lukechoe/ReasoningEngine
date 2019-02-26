
class KnowledgeBase(object):

    def __init__(self):
        self.facts = []
        self.rules = []

    def __repr__(self):
        return 'KnowledgeBase {!r}, {!r}'.format(self.facts, self.rules)
    # without inference
    def add(self, statement):
        if isinstance(statement, Fact):
            self.facts.append(statement)
        if isinstance(statement, Rule):
            self.rules.append(statement)
