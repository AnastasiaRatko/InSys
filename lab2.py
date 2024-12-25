class Tokenizer:
    def __init__(self, input_string):
        self.tokens = self._generate_tokens(input_string)
        self.current_position = 0

    def _generate_tokens(self, input_string):
        reserved_symbols = {
            ";", ")", "(", "&&", "||", "true", "false", "*", "/", "+", "-", "int", "bool", "char", "end", "const", "function"
        }
        words = input_string.split()
        token_list = []

        for word in words:
            token_list.append(self.get_token_type(word, reserved_symbols))

        token_list.append("end")
        return token_list

    def get_token_type(self, word, reserved_symbols):
        return ("const" * word.isdigit() or 
                "var:" * (word not in reserved_symbols) or 
                word)

    def current_token(self):
        return self.tokens[self.current_position] if self.current_position < len(self.tokens) else None

    def accept(self, expected_token):
        is_accepted = self.tokens[self.current_position] == expected_token
        self.current_position += is_accepted
        return is_accepted

    def raise_error(self, token, valid_tokens):
        should_raise = token not in valid_tokens
        if should_raise:
            raise ValueError(f"Ошибка синтаксиса: Неожиданный токен '{token}'. Допустимые токены: {valid_tokens}")

    def is_valid(self, token, valid_tokens):
        return token in valid_tokens


class StateHandler:
    def __init__(self, current_state, token, next_state, stack, tokenizer, valid_tokens):
        self.current_state = current_state
        self.token = token
        self.next_state = next_state
        self.stack = stack
        self.tokenizer = tokenizer
        self.valid_tokens = valid_tokens

    def handle_0_0_0_0(self):
        return self.next_state

    def handle_0_0_0_1(self):
        self.tokenizer.raise_error(self.token, self.valid_tokens)
        return self.next_state

    def handle_0_1_0_1(self):
        self.tokenizer.raise_error(self.token, self.valid_tokens)
        print(f"➔ Добавление состояния в стек: {self.current_state}")
        self.stack.append(self.current_state + 1)
        return self.next_state

    def handle_0_0_1_1(self):
        self.tokenizer.raise_error(self.token, self.valid_tokens)
        print(f"➔ Принятие токена: {self.token}")
        self.tokenizer.accept(self.token)
        return self.next_state

    def handle_1_0_0_1(self):
        self.tokenizer.raise_error(self.token, self.valid_tokens)
        popped_value = self.stack.pop() if self.stack else self.next_state
        print(f"➔ Извлечение из стека: {popped_value}")
        return popped_value

    def handle_1_0_1_1(self):
        self.tokenizer.raise_error(self.token, self.valid_tokens)
        print(f"➔ Принятие токена: {self.token}")
        self.tokenizer.accept(self.token)
        return self.stack.pop() if self.stack else self.next_state

class LL1:
    def __init__(self, transition_table):
        self.transition_table = transition_table
        self.current_state = 1
        self.stack = []
        self.tokenizer = None
        self.action_map = self._create_action_map(transition_table)

    def analyze(self, tokens):
        self.tokenizer = Tokenizer(" ".join(tokens))
        current_token = self.tokenizer.current_token()

        while current_token is not None:
            if current_token == 'end' and not self.stack:
                print("Парсинг завершен успешно.")
                break

            state_info = self.transition_table[self.current_state]
            print(f"{self.current_state} \t {current_token} \t Стек: {self.stack}")

            valid_tokens, next_state, ret, stack, accept, error = state_info

            if not self.tokenizer.is_valid(current_token, valid_tokens) and error == 0:
                print(f"Неожиданный токен '{current_token}' ➔ переход к состоянию {self.current_state + 1}")
                self.current_state += 1
                current_token = self.tokenizer.current_token()
                continue


            state_handler = StateHandler(self.current_state, current_token, next_state, self.stack, self.tokenizer, valid_tokens)
            action_method = self.action_map.get((ret, stack, accept, error), "handle_0_0_0_1")
            self.current_state = getattr(state_handler, action_method)()
            current_token = self.tokenizer.current_token()

        print("Грамматика верна")

    def _create_action_map(self, transition_table):
        action_map = {}
        for state, info in transition_table.items():
            ret, stack, accept, error = info[2:6]
            action_map[(ret, stack, accept, error)] = f"handle_{ret}_{stack}_{accept}_{error}"
        return action_map


transitions = {
    1: ['end ) ( const var: true false function && number', 19, 0, 0, 0, 1],
    2: ['* /', 22, 0, 0, 0, 0],
    3: ['end ) && ', 25, 0, 0, 0, 1],
    4: ['( const var: true false function number', 26, 0, 0, 0, 1],
    5: ['+ -', 28, 0, 0, 0, 0],
    6: ['* / ) && end', 31, 0, 0, 0, 1],
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
    17: ['&& ', 51, 0, 0, 0, 0],
    18: ['&& * / + - ) end', 53, 0, 0, 0, 1],
    19: ['( const var: true false function number', 4, 0, 1, 0, 1],
    20: ['* / ) end', 2, 0, 1, 0, 1],
    21: ['&& * / + - ) end', 17, 0, 0, 0, 1],
    22: ['* /', 23, 0, 0, 1, 1],
    23: ['( const var: true false function number', 4, 0, 1, 0, 1],
    24: ['* / ) && end', 2, 0, 0, 0, 1],
    25: ['end ) && ', -1, 1, 0, 0, 1],
    26: ['( const var: true false function number', 7, 0, 1, 0, 1],
    27: ['+ - * / ) && end', 5, 0, 0, 0, 0],
    28: ['+ -', 29, 0, 0, 1, 1],
    29: ['( const var: true false function number', 7, 0, 1, 0, 1],
    30: ['+ - * / ) end', 5, 0, 0, 0, 1],
    31: ['* / ) && end', -1, 1, 0, 0, 1],
    32: ['(', 33, 0, 0, 1, 1],
    33: ['end ) ( const var: true false function && number', 1, 0, 1, 0, 1],
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
    51: ['&& ', 52, 0, 0, 1, 1],
    52: ['end ) ( const var: true false function && number', 1, 0, 0, 0, 1],
    53: ['&& * / + - ) end', -1, 1, 0, 0, 1]
}

#nput_expression = "( 5 ) + 1"
tokenizer_instance = Tokenizer("( 5 ) + 1")
tokens = tokenizer_instance.tokens
parser_instance = LL1(transitions)
parser_instance.analyze(tokens)
