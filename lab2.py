from collections import deque

table = {
    #множество направляющих символов #next #return #stack #accept #error
    1: ['end ) ( const var: true false function && || number', 19, 0, 0, 0, 1],
    2: ['* /', 22, 0, 0, 0, 0],
    3: ['end ) && ||', 25, 0, 0, 0, 1],
    4: ['( const var: true false function number', 26, 0, 0, 0, 1],
    5: ['+ -', 28, 0, 0, 0, 0],
    6: ['* / ) && || end', 31, 0, 0, 0, 1],
    7: ['(', 32, 0, 0, 0, 0],
    8: ['const', 35, 0, 0, 0, 0],
    9: ['true false', 36, 0, 0, 0, 0],
    10: ['var:', 37, 0, 0, 0, 0],
    11: ['function', 38, 0, 0, 0, 1],
    12: ['function', 39, 0, 0, 0, 1],
    13: [';', 43, 0, 0, 0, 0],
    14: ['):', 46, 0, 0, 0, 1],
    15: ['var:', 48, 0, 0, 0, 1],
    16: ['int bool char', 50, 0, 0, 0, 1],
    17: ['&& ||', 51, 0, 0, 0, 0],
    18: ['&& || * / + - ) end', 53, 0, 0, 0, 1],
    19: ['( const var: true false function number', 4, 0, 1, 0, 1],
    20: ['* / ) end', 2, 0, 1, 0, 1],
    21: ['&& || * / + - ) end', 17, 0, 0, 0, 1],
    22: ['* /', 23, 0, 0, 1, 1],
    23: ['( const var: true false function number', 4, 0, 1, 0, 1],
    24: ['* / ) && || end', 2, 0, 0, 0, 1],
    25: ['end ) && ||', -1, 1, 0, 0, 1],
    26: ['( const var: true false function number', 7, 0, 1, 0, 1],
    27: ['+ - * / ) && || end', 5, 0, 0, 0, 0],
    28: ['+ -', 29, 0, 0, 1, 1],
    29: ['( const var: true false function number', 7, 0, 1, 0, 1],
    30: ['+ - * / ) end', 5, 0, 0, 0, 1],
    31: ['* / ) && || end', -1, 1, 0, 0, 1],
    32: ['(', 33, 0, 0, 1, 1],
    33: ['end ) ( const var: true false function && || number', 1, 0, 1, 0, 1],
    34: [')', -1, 1, 0, 1, 1],
    35: ['const', -1, 1, 0, 1, 1],
    36: ['true false', -1, 1, 0, 1, 1],
    37: ['var:', 15, 0, 0, 0, 1],
    38: ['function', 12, 0, 0, 0, 1],
    39: ['function', 40, 0, 0, 1, 1],
    40: ['(', 41, 0, 0, 1, 1],
    41: ['var:', 15, 0, 1, 0, 1],
    42: ['; ):', 13, 0, 0, 0, 1],
    43: [';', 44, 0, 0, 1, 1],
    44: ['var:', 15, 0, 1, 0, 1],
    45: ['; ):', 13, 0, 0, 0, 1],
    46: ['):', 47, 0, 0, 1, 1],
    47: ['int bool char', 16, 0, 0, 0, 1],
    48: ['var:', 49, 0, 0, 1, 1],
    49: ['int bool char', 16, 0, 0, 0, 1],
    50: ['int bool char', -1, 1, 0, 1, 1],
    51: ['&& ||', 52, 0, 0, 1, 1],
    52: ['end ) ( const var: true false function && || number', 1, 0, 0, 0, 1],
    53: ['&& || * / + - ) end', -1, 1, 0, 0, 1]
}



def analyze_expression(expression):
    state = 1
    tokens = expression.split() + ["end"]
    stack = deque()

    for token in tokens:
        accepted, error, end_of_expression = False, False, False

        while not (accepted or error or end_of_expression):
            end_of_expression = (token == "end" and (token in table[state][0]) and len(stack) == 0)

            token = "const" if token.isdigit() else token

            keywords = "; ): && || ) ( true false * / + - int bool char end const function".split()
            if token not in keywords and len(tokens) > 1:
                next_token = tokens[tokens.index(token) + 1]
                
                token = "function" if next_token == '(' else token
                token = "var:" if token not in keywords else token

            if token in table[state][0] and not end_of_expression:
                next_state = stack.pop() if table[state][2] == 1 else table[state][1]

                if table[state][3] == 1:
                    stack.append(state + 1)
                if table[state][4] == 1:
                    accepted = True
                    state = next_state
                    break
                state = next_state
            elif end_of_expression:
                break
            elif table[state][5] == 0:
                state += 1
            else:
                error = True
                break

        if error:
            print("-- Ошибка --")
            break
        if end_of_expression:
            print("-- Слово принадлежит данному языку --")
            break

analyze_expression("33 / 25 || 6")
analyze_expression("true * true && var: char + function ( var: int ): char")
analyze_expression("var: int + function ( var: bool ): bool")
