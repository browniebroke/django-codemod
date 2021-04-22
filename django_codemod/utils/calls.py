from typing import Optional, Sequence

from libcst import Arg, Call, FunctionDef, Param
from libcst import matchers as m
from libcst import parse_expression, parse_statement


def find_keyword_arg(args: Sequence[Arg], keyword_name: str) -> Optional[Arg]:
    """Find a kwarg among a sequence of arguments."""
    matcher = m.Arg(keyword=m.Name(keyword_name))
    for arg in args:
        if m.matches(arg, matcher):
            return arg
    return None


def parse_arg(arg_str: str) -> Arg:
    """Build a `Arg` instance based on its string representation.

    Instantiating it from scratch is cumbersome, this helper generates a
    function call with the given argument and extract it from the tree.
    """
    call_result = parse_expression(f"call({arg_str})")
    if isinstance(call_result, Call):
        return call_result.args[0]
    raise AssertionError(f"Unexpected type for: {call_result}")


def parse_param(arg_str: str) -> Param:
    """Build a `Param` instance based on its string representation.

    Instantiating it from scratch is cumbersome, this helper generates a
    function definition with the given param and extract it from the tree.
    """
    statement = parse_statement(f"def fun({arg_str}):...")
    if isinstance(statement, FunctionDef):
        return statement.params.params[0]
    raise AssertionError(f"Unexpected type for: {statement}")
