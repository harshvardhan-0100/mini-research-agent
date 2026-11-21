# def search_notes(query): 

#     with open("notes.txt", "r") as file: 
#         content = file.readlines()

#     results = []

#     for line in content: 
#         if query.lower() in line.lower(): 
#             results.append(line.strip())

#     if not results: 
#         return "No matching information found."

#     return "\n".join(results)


def search_notes(query): 

    with open("notes.txt", "r") as file: 
        content = file.readlines()


    # add stop words
    stop_words = {
        "what", "is", "the", "a", "an",
        "how", "why", "and", "or", "of",
        "to", "for", "in", "on", "with",
        "explain", "explained", "about"
    }
    #Convert query into indvl words
    query_words = [
        word.lower()
        for word in query.split()
        if word.lower() not in stop_words
    ]

    results = []

    for line in content: 

        line_lower = line.lower()

        #count how many query words appear in this line
        score = 0

        for word in query_words: 
            if word in line_lower: 
                score += 1

        if score > 0: 
            results.append((score, line.strip()))

    # sort results vy relevance score
    results.sort(reverse=True)

    if not results: 
        return "NO MATCHING INFORMATION FOUND."

    # return matching lines
    return "\n".join(
        line for score, line in results
    )


import ast
import operator

import ast
import operator


def calculate(expression):

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def evaluate(node):

        # Numbers
        if isinstance(node, ast.Constant):
            return node.value

        # Mathematical operations
        if isinstance(node, ast.BinOp):

            left = evaluate(node.left)
            right = evaluate(node.right)

            operator_function = operators[type(node.op)]

            return operator_function(left, right)

        raise ValueError("Unsupported expression")

    try:

        parsed_expression = ast.parse(expression, mode="eval")

        return evaluate(parsed_expression.body)

    except Exception as error:

        return f"Calculation error: {error}"



# print(calculate("25 * 4 + 10"))
# print(calculate("100 / 5"))
# print(calculate("2 ** 3"))
# print(calculate("10 - 3"))
    