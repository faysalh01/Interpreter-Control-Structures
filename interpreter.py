# Onyx Interpreter and Environment
# Part 4 - Programming Languages Project

from ast_nodes import (
    ProgramNode,
    NumberNode,
    VariableNode,
    BinaryOpNode,
    AssignmentNode,
    PrintNode,
    IfNode,
    WhileNode,
)


class Environment:
    """Environment / Symbol Table for managing variable storage and lookup."""
    def __init__(self):
        self.values = {}

    def get(self, name):
        if name in self.values:
            return self.values[name]
        raise RuntimeError(f"Runtime error: undefined variable '{name}'.")

    def set(self, name, value):
        self.values[name] = value


class Interpreter:
    """Interpreter that traverses the AST and executes Onyx statements."""
    def __init__(self):
        self.environment = Environment()
        self.output_buffer = []

    def interpret(self, node):
        self.output_buffer = []
        self.visit(node)
        return self.output_buffer

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        raise RuntimeError(f"No visit_{type(node).__name__} method defined for AST node.")

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_NumberNode(self, node):
        return node.value

    def visit_VariableNode(self, node):
        return self.environment.get(node.name)

    def visit_BinaryOpNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.operator == '+':
            return left_val + right_val
        elif node.operator == '-':
            return left_val - right_val
        elif node.operator == '*':
            return left_val * right_val
        elif node.operator == '/':
            if right_val == 0:
                raise RuntimeError("Runtime error: division by zero.")
            return left_val // int(right_val)
        elif node.operator == '==':
            return 1 if left_val == right_val else 0
        elif node.operator == '!=':
            return 1 if left_val != right_val else 0
        elif node.operator == '<':
            return 1 if left_val < right_val else 0
        elif node.operator == '>':
            return 1 if left_val > right_val else 0
        elif node.operator == '<=':
            return 1 if left_val <= right_val else 0
        elif node.operator == '>=':
            return 1 if left_val >= right_val else 0
        else:
            raise RuntimeError(f"Runtime error: unknown operator '{node.operator}'.")

    def visit_AssignmentNode(self, node):
        value = self.visit(node.expression)
        var_name = node.variable.name
        if not node.declaration:
            # Verify variable exists before reassignment
            self.environment.get(var_name)
        self.environment.set(var_name, value)

    def visit_PrintNode(self, node):
        value = self.visit(node.expression)
        self.output_buffer.append(str(value))
        print(value)

    def visit_IfNode(self, node):
        cond_val = self.visit(node.condition)
        if cond_val != 0:
            self.visit(node.if_body)
        elif node.else_body is not None:
            self.visit(node.else_body)

    def visit_WhileNode(self, node):
        while self.visit(node.condition) != 0:
            self.visit(node.body)
