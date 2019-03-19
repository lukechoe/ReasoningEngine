from important_objects import *
from util import *


class SuggestionBase(object):
    def __init__(self):
        self.suggestions = []

    def __repr__(self):
        return 'SuggestionBase {!r}'.format(self.suggestions)

    
