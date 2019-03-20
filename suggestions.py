from important_objects import *
from util import *
from kb import *
import copy

class SuggestionBase(object):
    def __init__(self, kb):
        self.suggestions = []
        self.kb = kb
        self.original_suggestions = None

    def __repr__(self):
        return 'SuggestionBase {!r}'.format(self.suggestions)

    def add(self, s):
        if isinstance(s, Suggestion):
            self.suggestions.append(s)
        else:
            print("Not a suggestion, try again.")

    def evaluate(self, question):



        if not isinstance(question, Question):
            print("Invalid input (suggestion)")
            return
        s = False
        for suggestion in self.suggestions:
            if question.suggestion_list[0] == suggestion.function_name:
                s = suggestion
        if s == False:
            print("suggestion not found")
            return

        for i in range(len(s.function)):
            if s.function[i] != question.suggestion_list[i]:
                self.update_suggestion(s, s.function[i], question.suggestion_list[i])

        result_bindings = []
        ans = self.evaluate_helper(s, None, result_bindings)

        return ans

    def evaluate_helper(self, s, prev_s, result_bindings):
        factCheck = False
        for subgoal in s.subgoals:
            # look through facts to see if subgoal can be reached
            for fact in self.kb.facts:
                ask1 = self.kb.ask(subgoal)
                if ask1 != False:
                    if ask1 not in result_bindings:
                        factCheck = True
                        result_bindings.append(ask1[0])
                        #self.update_suggestion(s, ask1[0].vars[0], ask1[0].constants[0])
                        #print(ask1[0].vars[0], "::::::::", ask1[0].constants[0])
                    break
            # if not, then look through suggestions recursively
            for suggestion in self.suggestions:
                if subgoal[0] == suggestion.function_name:
                    self.evaluate_helper(suggestion, s, result_bindings)
        # evaluate result-step, then go back to previous suggestion and update var
        evaluated = s.result_step[0]
        terms = s.result_step[1:]
        #simple, no calculations needed

        if len(terms) == 1:
            if terms[0][0] != '?':
                if prev_s != None:
                    self.update_suggestion(prev_s, evaluated, str(terms[0]))
            else:
                c = self.find_constant(terms[0], result_bindings)

                self.update_suggestion(s, evaluated, str(c))
                if prev_s != None:
                    self.update_suggestion(prev_s, evaluated, str(c))
        else:
            ans = 1
            calculations = []
            #print(terms, '0------')
            for i in range(len(terms)-1, -1, -1):

                if terms[i] == 'TimesFn':
                    total = ans
                    for num in calculations:
                        total = total * num
                    ans = total
                    calculations = []

                elif terms[i] == 'QuotientFn':
                    pass
                elif terms[i][0] == '?':
                    c = self.find_constant(terms[i], result_bindings)
                    calculations.append(float(c))
                else:
                    calculations.append(float(terms[i]))
            # take answer and update previous suggestion's var in result-step
            # ans now has the evaluated
            #b = Binding(evaluated, ans)

        if prev_s != None and len(terms) > 1:
            self.update_suggestion(s, evaluated, str(ans))
            self.update_suggestion(prev_s, evaluated, str(ans))
            #print(prev_s.result_step, '\n\n')
            #print(s.result_step)
        # we're at the beginning again.. evaluate the final result
        else:

            for e in result_bindings:
                self.update_suggestion(s, e.vars[0], e.constants[0])

            evaluate = s.result_step[0]
            terms = s.result_step[1:]

            if s.result_step[0][0] != '?' and len(terms) == 1:
                return s.result_step[0]

            else:
                # evaluate leftover arguments
                ans = 1
                calculations = []
                for i in range(len(terms)-1, -1, -1):
                    print(terms[i])
                    if terms[i] == 'TimesFn':
                        total = ans
                        for num in calculations:
                            total = total * num
                        ans = total
                        calculations = []
                    elif terms[i] == 'QuotientFn':
                        pass
                    elif terms[i][0] == '?':
                        pass
                    #    print("Shouldn't have variables at the end state, debug")
                    #    return
                    else:
                        calculations.append(float(terms[i]))

                self.update_suggestion(s, evaluated, str(ans))

                ans = s.result_step[0]

                return ans


    # this takes a suggestion and replaces any bindings from the parameters
    # of the question. e.g. -> caloriesIn ?obj ?count where ?obj = moon
    # will turn the other ?obj's into "moon"
    def update_suggestion(self, suggestion, var, const):
        for subgoal in suggestion.subgoals:
            for i in range(len(subgoal)):
                if subgoal[i] == var:
                    subgoal[i] = const
        for i in range(len(suggestion.result_step)):
            if suggestion.result_step[i] == var:
                suggestion.result_step[i] = const

    def find_constant(self, var, result_bindings):
        for b in result_bindings:
            for i in range(len(b.vars)):
                if b.vars[i] == var:
                    return b.constants[i]
        return False
