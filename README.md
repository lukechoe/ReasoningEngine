# ReasoningEngine

Luke Choe
3/21/2019

This is a reasoning engine with reimplementations of suggestion features in
the FIRE reasoning engine in Common Lisp.


EECS 344 Report:
My project took what I learned in class into something similar, but in a
different coding language. I chose to implement a rudimentary version of a
justification-based truth maintenance system. I then extended it to be able to
ask the JTMS questions. I chose to approach this project because the
fundamentals of how truth maintenance systems was interesting to me. I thought
that recreating this would help me get a better understanding and greater
appreciation for the code behind the TMS.

I decided to look through the Common Lisp code to get a good idea of where to
begin. After learning through that, I created a skeleton code base that would
help me organize my thoughts and make my code more readable. I wanted to
implement the more important parts of a JTMS. In this case, I implemented an
inference capabilities with antecedent and consequent justifications.

"main.py" has documented unit tests for the functionality of each part of my
code base.

I started with my "important_objects.py" file. This file has classes that
represent facts and rules in the knowledge base. These facts and rules each
have attributes that define each fact/rule. "parser.py" came next. This file
dealt with all of parsing from text files to python readable data. "util.py"
has functions that interpret the readable data into the appropriate classes.
"kb.py" is where the inference engine code was implemented. Facts and rules
can infer more facts and rules. These inferred facts and rules can infer more
facts and rules recursively. Each node in the JTMS is initially labeled "IN",
and there is well-founded support for each node. Nodes (facts and rules)
asserted from the text file will not have any antecedents. But they will have
consequents that will be inferred. Those inferred nodes will then have
antecedents and possibly more consequents (see main.py test 4 and 5).

"suggestions.py" includes a knowledge base from "kb.py" then expands by allowing
questions to be evaluated. There is a "question" class in "important_objects.py"
and the evaluate function in this file takes a question object and return an
answer similar to how FIRE reasoning engine returns answers to bote questions.
A given question prompts a suggestion. That suggestion evaluates its subgoals
recursively. This code is in my evaluate function in which a recursive stack
is used to depth-first search all suggestions. The leaf nodes are facts instead
of suggestions that return a binding to the parent node. This is done until the
traversal reaches the root node again (see "main.py" tests 6 and 7). At the root
node, all bindings will be evaluated to return an answer. Currently, only
"TimesFn" and "QuotientFn" are functional (multiply and divide). I used my
suggestions that I made for homework 4 and facts I asserted to test the
functionality. FIRE reasoning engine and this TMS both output the same result.

Running main.py will pass 7/7 tests. Text files and unit test 08 were added to
allow for custom data.
NOTE: If writing suggestions, put each subgoal on new line

Organizing my code into multiple different files and providing a skeleton code
for each function really made this project easier for me. It could be even
better if I planned out all of my logic on paper before coding. That way, I
could create objects and functions to be more reusable and simple to read.
Parsing was the hardest part for me. I had issues getting the parentheses in
Common Lisp to align with arrays in Python. Next time, I would use Python
libraries meant for Common Lisp (I did not know they existed until I finished
my parsing functions). I would also write more edge cases for my unit tests to
test for the many edge cases that I have not yet resolved.
