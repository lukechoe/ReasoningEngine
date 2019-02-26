from important_objects import *


def classify(kb, data):
    if not data:
        print("No data found")
        return False
    for element in data:
        if not element:
            print("Empty data found")
            return False
        if element[0] == "rule":
            print(element)
        else: # gonna be a fact
            kb.facts.append(Fact(element))
