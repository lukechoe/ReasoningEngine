from important_objects import *
import re


def tokenize_file(file):
    file = open(file, "r")

    result  = []

    left_parens = 0
    right_parens = 0

    tmp_lst = []

    for line in file:
        if not line or line[0] == '#' or line[0] == '\n':
            continue
        tmp_str = ""
        line = line.strip()

        for c in line:

            if c == "(":
                left_parens += 1
            elif c == ")":
                right_parens += 1
            elif c == " " and tmp_str != ' ':
                tmp_lst.append(tmp_str)
                #print(tmp_str)
                tmp_str = ""
            elif c == '\n':
                pass
            else:
                tmp_str += c
        tmp_lst.append(tmp_str)
        #print(left_parens, '------', right_parens)
        if left_parens == right_parens and tmp_str != " ":
            result.append(tmp_lst)
            tmp_lst = []
    if left_parens != right_parens:
        raise ValueError()

    file.close()
    return result


def tokenize_file2(file):
    file = open(file, "r")

    result  = []

    line = file.readline()
    while line:
        my_elems = []

        elems = line.strip()
        if (not elems) or elems[0] == ' ' or elems[0] == '#':
            line = file.readline()
            continue
        count = count_parens(line)
        if count[0] == count[1]: # if the statement has the same number of left and right parens on one line
            line = line.replace('(', ' ')
            line = line.replace(')', ' ')
            my_elems = line.split()
            result.append(my_elems)
            line = file.readline()
        else:
            while(count[0] != count[1]):
                count = count_parens(line)
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                tmp_lst = line.split()
                line = file.readline()
                my_elems.append(tmp_lst)
            result.append(my_elems)
    file.close()
    return result

def parse_line(text):
    pass


def count_parens(e):
    left_paren = 0
    right_paren = 0
    for c in e:
        if c == '(':
            left_paren += 1
        if c == ')':
            right_paren += 1
    return [left_paren, right_paren]

# Check and see if txt file statement is one line or multiple (return true if parens are balanced in one line)
def one_liner(e):
    left_paren = 0
    right_paren = 0
    for c in e:
        if c == '(':
            left_paren += 1
        if c == ')':
            right_paren += 1
    if left_paren == right_paren:
        return True
    else:
        return False



# Parse suggestions
def tokenize_suggestion_file(file):
    file = open(file, "r")
    list_of_suggestions = []
    single_suggestion = []
    line = file.readline()
    parts_of_suggestion = []
    while line:

        line = line.strip()
        if line == '':
            line = file.readline()
            continue
        if line[:9] == ':subgoals':
            line = line[10:]

            subgoal_lst = []
            while line:
                #print(line)
                if line[:12] == ':result-step':
                    break
                line = line.replace('(', '')
                line = line.replace(')', '')
                elems = line.split()
                subgoal_lst.append(elems)

                line = file.readline()
                line = line.strip()
            parts_of_suggestion.append(subgoal_lst)
            continue


        if line[0] == '(':
            line = line.replace('(', '')
            line = line.replace(')', '')
            elems = line.split()
            parts_of_suggestion.append(elems)
        if line[:12] == ":result-step":
            line = line[13:]
            line = line.replace('(', '')
            line = line.replace(')', '')
            elems = line.split()
            parts_of_suggestion.append(elems)

            list_of_suggestions.append(parts_of_suggestion)

            parts_of_suggestion = []
            single_suggestion = []

        line = file.readline()

    file.close()
    return list_of_suggestions
