from important_objects import *


def classify(kb, data):
    if not data:
        print("No data found")
        return False
    for element in data:
        if not element:
            print("Empty data found")
            return False
        if element[0] == "rule": # todo: GET THIS WORKING THEN DO BINDINGS
            ind = 0
            rule_lst = [] # holds a 2D array of all rules
            tmp_lst = [] # holds the elements of one rule
            for item in element:
                # ignore apostraphes and commas
                item = item.strip(',')
                item = item.strip('\'')

                if item == "rule" or item == "assert!":
                    if len(tmp_lst) > 0:
                        rule_lst.append(tmp_lst)
                        tmp_lst = []
                else:
                    tmp_lst.append(item)
            # make rule with left and right sides of rule
            # tmp_lst contains the assertion
            kb.add(Rule(rule_lst, tmp_lst))

        else: # gonna be a fact
            kb.add(Fact(element))

def classify_suggestions(sb, data):
    if not data:
        print("No data found")
        return False
    for suggestion in data:
        s = Suggestion(suggestion)
        sb.add(s)
