#!/usr/bin/env python3

import ast
import operator
import sys
from typing import Any


class SafeEvaluator:
    """Safely evaluate simple arithmetic expressions.

    Supported:
    - Binary operators: +, -, *, /
    - Unary operators: +, -
    - Parentheses via normal expression grouping
    - Integers and floats

    Disallowed:
    - Names, calls, attributes, comprehensions, etc.
    - Any non-arithmetic nodes
    """

    _binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        # If you want to allow these, uncomment and add tests:
        # ast.FloorDiv: operator.floordiv,
        # ast.Mod: operator.mod,
        # ast.Pow: operator.pow,
    }

    _unary_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate_expression(self, expression_text: str) -> float:
        try:
            expression_text = expression_text.strip()
            parsed = ast.parse(expression_text, mode="eval")
        except SyntaxError as syntax_error:
            raise ValueError(f"Invalid expression: {syntax_error}") from syntax_error

        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node: ast.AST) -> Any:
        if isinstance(node, ast.BinOp):
            return self._evaluate_binop(node)
        if isinstance(node, ast.UnaryOp):
            return self._evaluate_unaryop(node)
        if isinstance(node, ast.Num):  # Python <3.8 compatibility
            return node.n
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only integers and floats are allowed as literals")
        if isinstance(node, ast.Expr):
            return self._evaluate_node(node.value)

        # Allow parentheses implicitly; they just structure the AST
        if isinstance(node, ast.Tuple) and len(node.elts) == 1:
            return self._evaluate_node(node.elts[0])

        # Explicitly reject everything else
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    def _evaluate_binop(self, node: ast.BinOp) -> Any:
        left_value = self._evaluate_node(node.left)
        right_value = self._evaluate_node(node.right)
        op_type = type(node.op)
        if op_type not in self._binary_ops:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return self._binary_ops[op_type](left_value, right_value)

    def _evaluate_unaryop(self, node: ast.UnaryOp) -> Any:
        operand_value = self._evaluate_node(node.operand)
        op_type = type(node.op)
        if op_type not in self._unary_ops:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return self._unary_ops[op_type](operand_value)


def evaluate(expression_text: str) -> float:
    """Public helper to evaluate an expression string safely."""
    evaluator = SafeEvaluator()
    return evaluator.evaluate_expression(expression_text)


def _print_usage() -> None:
    usage = (
        "Simple Calculator\n\n"
        "Usage:\n"
        "  python3 calculator.py \"2 + 3 * 4\"\n"
        "  ./calculator.py \"(1 + 2) / 3\"\n\n"
        "Interactive mode (REPL):\n"
        "  python3 calculator.py\n"
        "  Type expressions using +, -, *, / and parentheses. Type 'quit' or press Ctrl-D to exit.\n"
    )
    print(usage)


def repl() -> int:
    evaluator = SafeEvaluator()
    print("Simple Calculator. Type 'quit' to exit.")
    while True:
        try:
            line = input("calc> ").strip()
        except EOFError:
            print()
            return 0

        if line.lower() in {"quit", "exit"}:
            return 0
        if not line:
            continue
        try:
            result = evaluator.evaluate_expression(line)
            print(result)
        except Exception as error:  # noqa: BLE001 - show friendly error
            print(f"Error: {error}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        sys.exit(repl())
    if argv and argv[0] in {"-h", "--help"}:
        _print_usage()
        sys.exit(0)

    expression = " ".join(argv)
    try:
        print(evaluate(expression))
    except Exception as error:  # noqa: BLE001
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)