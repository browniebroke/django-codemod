"""Main module."""
from typing import Union

from libcst import RemovalSentinel, Call, BaseExpression, Name
from libcst._nodes.statement import Import, ImportFrom, BaseSmallStatement, ImportAlias
from libcst.codemod import VisitorBasedCodemodCommand


class ForceTextToStrCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Replaces force_text() by force_str()."

    def leave_Import(
        self, original_node: Import, updated_node: Import
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        return super().leave_Import(original_node, updated_node)

    def leave_ImportFrom(
        self, original_node: ImportFrom, updated_node: ImportFrom
    ) -> Union[BaseSmallStatement, RemovalSentinel]:
        if updated_node.module and len(updated_node.module.children) == 3:
            tops, _, last = updated_node.module.children
            top, _, middle = tops.children
            if (
                top.value == "django"
                and middle.value == "utils"
                and last.value == "encoding"
            ):
                new_names = []
                new_import_missing = True
                new_import_alias = None
                for import_alias in original_node.names:
                    if import_alias.evaluated_name == "force_text":
                        new_import_alias = ImportAlias(name=Name("force_str"))
                    else:
                        if import_alias.evaluated_name == "force_str":
                            new_import_missing = False
                        new_names.append(import_alias)
                if new_import_missing and new_import_alias is not None:
                    new_names.append(new_import_alias)
                new_names = list(sorted(new_names, key=lambda n: n.evaluated_name))
                return ImportFrom(module=updated_node.module, names=new_names)
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        if updated_node.func.value == "force_text":
            return Call(args=updated_node.args, func=Name("force_str"))
        return super().leave_Call(original_node, updated_node)
