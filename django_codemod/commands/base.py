"""Module to implement base functionality."""
from abc import ABC
from typing import List

import libcst as cst
from libcst.codemod import VisitorBasedCodemodCommand, ContextAwareTransformer


class BaseCodemodCommand(VisitorBasedCodemodCommand, ABC):
    """Base class for our commands."""

    transformers: List[ContextAwareTransformer]

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        for transform in self.transformers:
            inst = transform(self.context)
            tree = inst.transform_module(tree)
        return tree
