import lexer
import sys

class parser_state():
    def __init__ (self, tokens, pos=0):
        self.tokens = tokens
        self.pos = pos

    def inc_position(self):
        self.pos += 1
    def jump_position(self, index):
        self.pos = index

    def add_output(self, out):
        self.output += out

    def get_token_type(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][1]
        else:
            return None
    def get_token_val(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        else:
            return None
    def get_token_len(self):
        return len(self.tokens)
    def get_pos(self):
        return self.pos

def parse(input):
    tokens = init_tokens(input)
    state = parser_state(tokens)

    while state.get_pos() < state.get_token_len():
        res = parse_variable_declaration(state)
        if res is not None:
            state = res
        state.inc_position()

def init_tokens(input):

    RESERVED = 'RESERVED'
    INT      = 'INT'
    ID       = 'ID'
    SIZE     = 'SIZE'
    
    token_exprs = [
        (r'[ \n\t]+',              None),
        (r'#[^\n]*',               None),
        (r'\=',                    RESERVED),
        (r'\:',                    RESERVED),
        (r'\(',                    RESERVED),
        (r'\)',                    RESERVED),
        (r'\{',                    RESERVED),
        (r'\}',                    RESERVED),
        (r';',                     RESERVED),
        (r'\+',                    RESERVED),
        (r'-',                     RESERVED),
        (r'\*',                    RESERVED),
        (r'/',                     RESERVED),
        (r'<=',                    RESERVED),
        (r'<',                     RESERVED),
        (r'>=',                    RESERVED),
        (r'>',                     RESERVED),
        (r'=',                     RESERVED),
        (r'!=',                    RESERVED),
        (r'&&',                    RESERVED),
        (r'\|\|',                  RESERVED),
        (r'!',                     RESERVED),
        (r'if',                    RESERVED),
        (r'then',                  RESERVED),
        (r'else',                  RESERVED),
        (r'while',                 RESERVED),
        (r'qword',                 SIZE),
        (r'dword',                 SIZE),
        (r'word',                  SIZE),
        (r'byte',                  SIZE),
        (r'[0-9]+',                INT),
        (r'[A-Za-z][A-Za-z0-9_]*', ID)
    ]

    return lexer.lex(input, token_exprs)


def parse_variable_declaration(state):
    if state.get_token_type() != 'SIZE':
        return None
    state.inc_position()
    if state.get_token_type() != 'ID':
        throw_parse_error("Expected a variable name", state)
        return None
    state.inc_position()
    if state.get_token_val() != ':':
        throw_parse_error("Expected a colon", state)
        return None
    state.inc_position()
    if state.get_token_type() != 'ID':
        throw_parse_error("Expected a type", state)
        return None
    state.inc_position()
    if state.get_token_val() == '=':
        state.inc_position()
        res = parse_expression(state)
        if res is None:
            throw_parse_error("Expected a value", state)
            return None
        else:
            return state
    else:
        return state

def parse_expression(state):
    throw_parse_error("Expected a variable or literals", state)
    return None


def throw_parse_error(msg, state):
    sys.stderr.write("Error: %s at token %s \n" % (msg, state.get_pos()+1))

def throw_EOF_error(msg):
    sys.stderr.write("Error: %s \n" % msg)
    sys.exit(1)