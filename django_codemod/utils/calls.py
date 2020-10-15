from typing import Optional

from libcst import Arg
from libcst import matchers as m


def find_keyword_arg(args, keyword_name: str) -> Optional[Arg]:
    matcher = m.Arg(keyword=m.Name(keyword_name))
    for arg in args:
        if m.matches(arg, matcher):
            return arg
    return None
