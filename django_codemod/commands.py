from abc import ABC
from typing import List, Type

import libcst as cst
from libcst.codemod import (
    CodemodContext,
    ContextAwareTransformer,
    VisitorBasedCodemodCommand,
)


class BaseCodemodCommand(VisitorBasedCodemodCommand, ABC):
    """Base class for our commands."""

    transformers: List[Type[ContextAwareTransformer]]

    def __init__(self, transformers, context: CodemodContext) -> None:
        self.transformers = transformers
        super().__init__(context)

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        for transform in self.transformers:
            inst = transform(self.context)
            tree = inst.transform_module(tree)
        return tree
