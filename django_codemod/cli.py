import inspect
from abc import ABC
from typing import List

import click
from libcst.codemod import (
    CodemodContext,
    ContextAwareTransformer,
    gather_files,
    parallel_exec_transform_with_prettyprint,
)

from django_codemod.commands.base import BaseCodemodCommand
from django_codemod.visitors import django_30, django_40


class VersionParamType(click.ParamType):
    """A type of parameter to parse Versions as arguments."""

    name = "version"
    example = (
        "Should include the major & minor digits of the Django version"
        " e.g. '2.2' or '2.2.10'"
    )

    def convert(self, value, param, ctx):
        """Parse version to keep only major an minor digits."""
        try:
            return self._parse_unsafe(value, param, ctx)
        except TypeError:
            self.fail(
                f"{value!r} unable to parse version. {self.example}", param, ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid version. {self.example}", param, ctx)

    def _parse_unsafe(self, value, param, ctx):
        """Parse version and validate it's a supported one."""
        parsed_version = self._split_digits(value, param, ctx)
        if parsed_version not in VERSIONS_MODIFIERS.keys():
            supported_versions = ", ".join(
                ".".join(str(version_part) for version_part in version_tuple)
                for version_tuple in VERSIONS_MODIFIERS.keys()
            )
            self.fail(
                f"{value!r} is not supported. "
                f"Versions supported: {supported_versions}",
                param,
                ctx,
            )
        return parsed_version

    def _split_digits(self, value, param, ctx):
        """Split version into 2-tuple of digits, ignoring patch digit."""
        values_parts = tuple(int(v) for v in value.split("."))
        if len(values_parts) < 2:
            self.fail(
                f"{value!r} missing version parts. {self.example}", param, ctx,
            )
        major, minor, *patches = values_parts
        return (major, minor)


DJANGO_VERSION = VersionParamType()

VERSIONS_MODIFIERS = {
    (3, 0): django_30,
    # (3, 1): django_31,
    # (3, 2): django_32,
    (4, 0): django_40,
}


@click.command()
@click.argument("path")
@click.option(
    "--removed-in",
    "removed_in",
    help="The version of Django to fix deprecations for.",
    type=DJANGO_VERSION,
    required=True,
)
def djcodemod(removed_in, path):
    """
    Automatically fixes deprecations removed Django deprecations.

    This command takes the path to target as argument and a version of
    Django where a previously deprecated feature is removed.
    """
    codemod_modules_list = [VERSIONS_MODIFIERS[removed_in]]
    command_instance = build_command(codemod_modules_list)
    call_command(command_instance, path)


def build_command(codemod_modules_list: List) -> BaseCodemodCommand:
    """Build a custom command with the list of visitors."""
    codemodders_list = []
    for codemod_module in codemod_modules_list:
        for objname in dir(codemod_module):
            try:
                obj = getattr(codemod_module, objname)
                if (
                    obj is ContextAwareTransformer
                    or not issubclass(obj, ContextAwareTransformer)
                    or inspect.isabstract(obj)
                ):
                    continue
                # isabstract is broken for direct subclasses of ABC which
                # don't themselves define any abstract methods, so lets
                # check for that here.
                if any(cls[0] is ABC for cls in inspect.getclasstree([obj])):
                    continue
                # Looks like this one is good to go
                codemodders_list.append(obj)
            except TypeError:
                continue

    class CustomCommand(BaseCodemodCommand):
        transformers = codemodders_list

    return CustomCommand(CodemodContext())


def call_command(command_instance: BaseCodemodCommand, path: str):
    """Call libCST with our customized command."""
    files = gather_files(path)
    try:
        # Super simplified call
        result = parallel_exec_transform_with_prettyprint(
            command_instance,
            files,
            # Number of jobs to use when processing files. Defaults to number of cores
            jobs=None,
        )
    except KeyboardInterrupt:
        raise click.Abort("Interrupted!")

    # fancy summary a-la libCST
    total = result.successes + result.skips + result.failures
    click.echo(f"Finished codemodding {total} files!")
    click.echo(f" - Transformed {result.successes} files successfully.")
    click.echo(f" - Skipped {result.skips} files.")
    click.echo(f" - Failed to codemod {result.failures} files.")
    click.echo(f" - {result.warnings} warnings were generated.")
    if result.failures > 0:
        raise click.exceptions.Exit(1)


if __name__ == "__main__":
    djcodemod()
