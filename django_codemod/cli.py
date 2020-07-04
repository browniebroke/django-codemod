import inspect
from collections import defaultdict
from operator import attrgetter
from typing import Callable, Dict, List, Tuple

import click
from libcst.codemod import (
    CodemodContext,
    ContextAwareTransformer,
    gather_files,
    parallel_exec_transform_with_prettyprint,
)

from django_codemod import visitors
from django_codemod.commands import BaseCodemodCommand


def find_codemoders(version_getter: Callable) -> Dict[Tuple[int, int], List]:
    """
    Find codemodders and index them by version.

    The returned entity is a dictionary which keys are 2-tuples
    for each major versions of Django with codemodders mapping
    to a list of codemodders which are flagged as either `removed_in`
    or `deprecated_in` that version.
    """
    codemodders_index = defaultdict(list)
    for object_name in dir(visitors):
        try:
            obj = getattr(visitors, object_name)
            if (
                obj is ContextAwareTransformer
                or not issubclass(obj, ContextAwareTransformer)
                or inspect.isabstract(obj)
            ):
                continue
            # Looks like this one is good to go
            django_version = version_getter(obj)
            codemodders_index[django_version].append(obj)
        except TypeError:
            continue
    return dict(codemodders_index)


DEPRECATED_IN = find_codemoders(version_getter=attrgetter("deprecated_in"))
REMOVED_IN = find_codemoders(version_getter=attrgetter("removed_in"))


class VersionParamType(click.ParamType):
    """A type of parameter to parse Versions as arguments."""

    name = "version"
    example = (
        "Should include the major & minor digits of the Django version"
        " e.g. '2.2' or '2.2.10'"
    )

    def __init__(self, version_index) -> None:
        self.valid_versions = version_index.keys()

    def convert(self, value, param, ctx):
        """Parse version to keep only major an minor digits."""
        try:
            return self._parse_unsafe(value, param, ctx)
        except ValueError:
            self.fail(f"{value!r} is not a valid version. {self.example}", param, ctx)

    def _parse_unsafe(self, value, param, ctx):
        """Parse version and validate it's a supported one."""
        parsed_version = self._split_digits(value, param, ctx)
        if parsed_version not in self.valid_versions:
            supported_versions = ", ".join(
                ".".join(str(version_part) for version_part in version_tuple)
                for version_tuple in self.valid_versions
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


@click.command()
@click.argument("path")
@click.option(
    "--removed-in",
    "removed_in",
    help="The version of Django where feature are removed.",
    type=VersionParamType(REMOVED_IN),
)
@click.option(
    "--deprecated-in",
    "deprecated_in",
    help="The version of Django where deprecations started.",
    type=VersionParamType(DEPRECATED_IN),
)
def djcodemod(removed_in, deprecated_in, path):
    """
    Automatically fixes deprecations removed Django deprecations.

    This command takes the path to target as argument and a version of
    Django to select code modifications to apply.
    """
    if not any((removed_in, deprecated_in)) or all((removed_in, deprecated_in)):
        raise click.UsageError(
            "You must specify either '--removed-in' or '--deprecated-in' but not both."
        )
    if removed_in:
        codemodders_list = REMOVED_IN[removed_in]
    else:
        codemodders_list = DEPRECATED_IN[deprecated_in]
    command_instance = build_command(codemodders_list)
    call_command(command_instance, path)


def build_command(codemodders_list: List) -> BaseCodemodCommand:
    """Build a custom command with the list of visitors."""

    class CustomCommand(BaseCodemodCommand):
        transformers = codemodders_list

    return CustomCommand(CodemodContext())


def call_command(command_instance: BaseCodemodCommand, path: str):
    """Call libCST with our customized command."""
    files = gather_files([path])
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
