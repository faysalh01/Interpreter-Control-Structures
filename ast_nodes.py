# Onyx Abstract Syntax Tree (AST)
# Part 4 - Programming Languages Project

class ASTNode:
    """Base class for all Onyx AST nodes."""
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({self.statements!r})"


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"NumberNode({self.value})"


class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name!r})"


class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.operator!r}, {self.left!r}, {self.right!r})"


class AssignmentNode(ASTNode):
    def __init__(self, variable, expression, declaration=True):
        self.variable = variable
        self.expression = expression
        self.declaration = declaration

    def __repr__(self):
        kind = "let" if self.declaration else "assign"
        return f"AssignmentNode({kind!r}, {self.variable!r}, {self.expression!r})"


class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode({self.expression!r})"


class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def __repr__(self):
        return f"IfNode({self.condition!r}, {self.if_body!r}, {self.else_body!r})"


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition!r}, {self.body!r})"
