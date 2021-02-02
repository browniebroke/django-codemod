from typing import List, Optional

from libcst import BaseExpression, Call, ImportFrom, ImportStar, MaybeSentinel, Module
from libcst import matchers as m

from django_codemod.constants import DJANGO_1_9, DJANGO_2_0
from django_codemod.visitors.base import BaseDjCodemodTransformer, import_from_matches


class SignalDisconnectWeakTransformer(BaseDjCodemodTransformer):
    """Remove the `weak` argument to `Signal.disconnect()`."""

    deprecated_in = DJANGO_1_9
    removed_in = DJANGO_2_0

    ctx_key_prefix = "SignalDisconnectWeakTransformer"
    ctx_key_call_matchers = f"{ctx_key_prefix}-call_matchers"
    builtin_signals = [
        "pre_init",
        "post_init",
        "pre_save",
        "post_save",
        "pre_delete",
        "post_delete",
        "m2m_changed",
        "pre_migrate",
        "post_migrate",
    ]
    import_alias_matcher = m.OneOf(
        *(m.ImportAlias(name=m.Name(signal_name)) for signal_name in builtin_signals)
    )

    @property
    def disconnect_call_matchers(self) -> List[m.Call]:
        return self.context.scratch.get(self.ctx_key_call_matchers, [])

    def add_disconnect_call_matcher(self, call_matcher: m.Call) -> None:
        self.context.scratch[
            self.ctx_key_call_matchers
        ] = self.disconnect_call_matchers + [call_matcher]

    def leave_Module(self, original_node: Module, updated_node: Module) -> Module:
        """Clear context when leaving module."""
        self.context.scratch.pop(self.ctx_key_call_matchers, None)
        return super().leave_Module(original_node, updated_node)

    def visit_ImportFrom(self, node: ImportFrom) -> Optional[bool]:
        """Set the `Call` matcher depending on which signals are imported.."""
        if not import_from_matches(
            node, ["django", "db", "models", "signals"]
        ) or isinstance(node.names, ImportStar):
            return False
        for import_alias in node.names:
            if m.matches(import_alias, self.import_alias_matcher):
                # We're visiting an import statement for a built-in signal
                # Get the actual name it's imported as (in case of import alias)
                imported_name_str = (
                    import_alias.evaluated_alias or import_alias.evaluated_name
                )
                # Add the call matcher for the current signal to the list
                self.add_disconnect_call_matcher(
                    m.Call(
                        func=m.Attribute(
                            value=m.Name(imported_name_str),
                            attr=m.Name("disconnect"),
                        ),
                    )
                )
        return None

    def leave_Call(self, original_node: Call, updated_node: Call) -> BaseExpression:
        """
        Remove the `weak` argument if present in the call.

        This is only changing calls with keyword arguments.
        """
        if self.disconnect_call_matchers and m.matches(
            updated_node, m.OneOf(*self.disconnect_call_matchers)
        ):
            updated_args = []
            should_change = False
            last_comma = MaybeSentinel.DEFAULT
            # Keep all arguments except the one with the keyword `weak` (if present)
            for index, arg in enumerate(updated_node.args):
                if m.matches(arg, m.Arg(keyword=m.Name("weak"))):
                    # An argument with the keyword `weak` was found
                    # -> we need to rewrite the statement
                    should_change = True
                else:
                    updated_args.append(arg)
                last_comma = arg.comma  # type: ignore
            if should_change:
                # Make sure the end of line is formatted as initially
                updated_args[-1] = updated_args[-1].with_changes(comma=last_comma)
                return updated_node.with_changes(args=updated_args)
        return super().leave_Call(original_node, updated_node)
