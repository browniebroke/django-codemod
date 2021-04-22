from typing import Optional, Sequence

from libcst import Arg, Call
from libcst import matchers as m
from libcst import parse_expression


def find_keyword_arg(args: Sequence[Arg], keyword_name: str) -> Optional[Arg]:
    """Find a kwarg among a sequence of arguments."""
    matcher = m.Arg(keyword=m.Name(keyword_name))
    for arg in args:
        if m.matches(arg, matcher):
            return arg
    return None


def make_kwarg(arg_str: str) -> Arg:
    """Helper to add simple kwarg to a function call.

    By default, libCST adds some spaces around the equal sign:

        func(name = value)

    This helper builds it without spaces:

        func(name=value)
    """
    call_result = parse_expression(f"call({arg_str})")
    if isinstance(call_result, Call):
        return call_result.args[0]
    raise AssertionError(f"Unexpected type for: {call_result}")
