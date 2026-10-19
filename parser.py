"""
Onyx Parser
Part 4 - Parser & Abstract Syntax Tree with Control Structures

Gunner's Part 4 contribution: extended recursive-descent parser supporting
comparisons, if/else statements, and while loops.
"""

from lexer import Lexer, LexerError
from ast_nodes import (
    ProgramNode,
    NumberNode,
    VariableNode,
    BinaryOpNode,
    AssignmentNode,
    PrintNode,
    IfNode,
    WhileNode,
    print_ast,
)


class ParserError(Exception):
    """Raised when Onyx source contains invalid syntax."""

    def __init__(self, message, position=None, token=None):
        self.position = position
        self.token = token
        if position is not None:
            message = f"Syntax error at token {position}: {message}"
        super().__init__(message)


class Parser:
    """Recursive-descent parser for the Part 4 Onyx grammar."""

    OPERATOR_SYMBOLS = {
        "PLUS": "+",
        "MINUS": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
    }

    COMPARISON_SYMBOLS = {
        "EQUAL_EQUAL": "==",
        "NOT_EQUAL": "!=",
        "LESS_THAN": "<",
        "GREATER_THAN": ">",
        "LESS_EQUAL": "<=",
        "GREATER_EQUAL": ">=",
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def is_at_end(self):
        return self.position >= len(self.tokens)

    def current(self):
        return None if self.is_at_end() else self.tokens[self.position]

    def advance(self):
        token = self.current()
        if not self.is_at_end():
            self.position += 1
        return token

    def check(self, token_type):
        token = self.current()
        return token is not None and token.token_type == token_type

    def match(self, *token_types):
        if self.current() is not None and self.current().token_type in token_types:
            return self.advance()
        return None

    @staticmethod
    def describe_token(token):
        if token is None:
            return "end of input"
        if token.value is not None:
            return f"{token.token_type}({token.value})"
        return token.token_type

    def expect(self, token_type, description=None):
        token = self.current()
        expected = description or token_type

        if token is None:
            raise ParserError(
                f"expected {expected}, but reached end of input.",
                self.position,
            )

        if token.token_type != token_type:
            raise ParserError(
                f"expected {expected}, found {self.describe_token(token)}.",
                self.position,
                token,
            )

        return self.advance()

    def parse(self):
        """Parse the entire token stream and require complete consumption."""
        program = self.parse_program()
        if not self.is_at_end():
            token = self.current()
            raise ParserError(
                f"unexpected {self.describe_token(token)} after complete statement.",
                self.position,
                token,
            )
        return program

    def parse_program(self):
        """program ::= { statement }"""
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_block(self):
        """parses statements inside { ... } until '}'"""
        statements = []
        while not self.is_at_end() and not self.check("RBRACE"):
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        """statement ::= assignment | print-statement | if-statement | while-statement"""
        if self.check("LET"):
            return self.parse_assignment(declaration=True)
        if self.check("PRINT"):
            return self.parse_print()
        if self.check("IF"):
            return self.parse_if()
        if self.check("WHILE"):
            return self.parse_while()
        if self.check("ID"):
            return self.parse_assignment(declaration=False)

        token = self.current()
        raise ParserError(
            "expected a statement (LET, PRINT, IF, WHILE, or assignment), "
            f"found {self.describe_token(token)}.",
            self.position,
            token,
        )

    def parse_assignment(self, declaration):
        """assignment ::= "let" identifier "=" expression ";" | identifier "=" expression ";" """
        if declaration:
            self.expect("LET", "'let'")

        name_token = self.expect("ID", "an identifier")
        self.expect("ASSIGN", "'='")
        expression = self.parse_expression()
        self.expect("SEMICOLON", "';'")

        return AssignmentNode(
            VariableNode(name_token.value),
            expression,
            declaration=declaration,
        )

    def parse_print(self):
        """print-statement ::= "print" "(" expression ")" ";" """
        self.expect("PRINT", "'print'")
        self.expect("LPAREN", "'('")
        expression = self.parse_expression()
        self.expect("RPAREN", "')'")
        self.expect("SEMICOLON", "';'")
        return PrintNode(expression)

    def parse_if(self):
        """if-statement ::= "if" "(" expression ")" "{" program "}" [ "else" "{" program "}" ] """
        self.expect("IF", "'if'")
        self.expect("LPAREN", "'('")
        condition = self.parse_expression()
        self.expect("RPAREN", "')'")

        self.expect("LBRACE", "'{'")
        if_body = self.parse_block()
        self.expect("RBRACE", "'}'")

        else_body = None
        if self.check("ELSE"):
            self.advance()
            self.expect("LBRACE", "'{'")
            else_body = self.parse_block()
            self.expect("RBRACE", "'}'")

        return IfNode(condition, if_body, else_body)

    def parse_while(self):
        """while-statement ::= "while" "(" expression ")" "{" program "}" """
        self.expect("WHILE", "'while'")
        self.expect("LPAREN", "'('")
        condition = self.parse_expression()
        self.expect("RPAREN", "')'")

        self.expect("LBRACE", "'{'")
        body = self.parse_block()
        self.expect("RBRACE", "'}'")

        return WhileNode(condition, body)

    def parse_expression(self):
        """expression ::= arithmetic-expr [ comparison-operator arithmetic-expr ]"""
        node = self.parse_arithmetic()

        comparison_tokens = list(self.COMPARISON_SYMBOLS.keys())
        operator = self.match(*comparison_tokens)
        if operator is not None:
            right = self.parse_arithmetic()
            node = BinaryOpNode(
                self.COMPARISON_SYMBOLS[operator.token_type],
                node,
                right,
            )

        return node

    def parse_arithmetic(self):
        """arithmetic-expr ::= term { ("+" | "-") term }"""
        node = self.parse_term()

        while True:
            operator = self.match("PLUS", "MINUS")
            if operator is None:
                break

            right = self.parse_term()
            node = BinaryOpNode(
                self.OPERATOR_SYMBOLS[operator.token_type],
                node,
                right,
            )

        return node

    def parse_term(self):
        """term ::= factor { ("*" | "/") factor }"""
        node = self.parse_factor()

        while True:
            operator = self.match("MULTIPLY", "DIVIDE")
            if operator is None:
                break

            right = self.parse_factor()
            node = BinaryOpNode(
                self.OPERATOR_SYMBOLS[operator.token_type],
                node,
                right,
            )

        return node

    def parse_factor(self):
        """factor ::= number | identifier | "(" expression ")" """
        token = self.current()

        if token is None:
            raise ParserError(
                "expected a number, variable, or parenthesized expression, "
                "but reached end of input.",
                self.position,
            )

        if token.token_type == "NUMBER":
            self.advance()
            return NumberNode(token.value)

        if token.token_type == "ID":
            self.advance()
            return VariableNode(token.value)

        if token.token_type == "LPAREN":
            self.advance()
            expression = self.parse_expression()
            self.expect("RPAREN", "')'")
            return expression

        raise ParserError(
            "expected a number, variable, or parenthesized expression; "
            f"found {self.describe_token(token)}.",
            self.position,
            token,
        )


def parse_source(source):
    """Lex and parse one complete Onyx source string."""
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


if __name__ == "__main__":
    example = "if (x >= 10) { print(x); } else { print(0); }"
    print(f"Source: {example}")
    try:
        tree = parse_source(example)
        print_ast(tree)
    except (LexerError, ParserError) as error:
        print(error)
