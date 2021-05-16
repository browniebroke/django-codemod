import inspect
from collections import defaultdict
from operator import attrgetter
from pathlib import Path
from typing import Callable, Dict, Generator, List, Optional, Tuple, Type

import click
from libcst.codemod import CodemodContext, parallel_exec_transform_with_prettyprint
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from django_codemod import visitors
from django_codemod.commands import BaseCodemodCommand
from django_codemod.path_utils import get_sources
from django_codemod.visitors.base import BaseDjCodemodTransformer


def index_codemodders(version_getter: Callable) -> Dict[Tuple[int, int], List]:
    """
    Index codemodders by version.

    Build a map of Django version to list of codemodders.
    """
    codemodders_index: defaultdict = defaultdict(list)
    for obj in iter_codemodders():
        django_version = version_getter(obj)
        codemodders_index[django_version].append(obj)
    return dict(codemodders_index)


def iter_codemodders() -> Generator[Type[BaseDjCodemodTransformer], None, None]:
    """Iterator of all the codemodders classes."""
    for object_name in dir(visitors):
        try:
            obj = getattr(visitors, object_name)
            if issubclass(obj, BaseDjCodemodTransformer) and not inspect.isabstract(
                obj
            ):
                yield obj  # Looks like this one is good to go
        except TypeError:
            continue


DEPRECATED_IN = index_codemodders(version_getter=attrgetter("deprecated_in"))
REMOVED_IN = index_codemodders(version_getter=attrgetter("removed_in"))
BY_NAME = {cls.__name__: cls for cls in iter_codemodders()}


class CodemodChoice(click.Choice):
    def get_metavar(self, param: click.Parameter) -> str:
        return "(see `djcodemod list`)"


class VersionParamType(click.ParamType):
    """A type of parameter to parse version as arguments."""

    name = "version"
    example = (
        "Should include the major & minor digits of the Django version"
        " e.g. '2.2' or '2.2.10'"
    )

    def __init__(self, version_index: Dict[Tuple[int, int], List]) -> None:
        self.valid_versions: List[Tuple[int, int]] = list(version_index.keys())

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Tuple[int, int]:
        """Parse version to keep only major an minor digits."""
        try:
            return self._parse_unsafe(value, param, ctx)
        except ValueError:
            self.fail(f"{value!r} is not a valid version. {self.example}", param, ctx)

    def _parse_unsafe(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Tuple[int, int]:
        """Parse version and validate it's a supported one."""
        parsed_version = self._split_digits(value, param, ctx)
        if parsed_version not in self.valid_versions:
            supported_versions = ", ".join(
                ".".join(str(version_part) for version_part in version_tuple)
                for version_tuple in sorted(self.valid_versions)
            )
            self.fail(
                f"{value!r} is not supported. "
                f"Versions supported: {supported_versions}",
                param,
                ctx,
            )
        return parsed_version

    def _split_digits(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Tuple[int, int]:
        """Split version into 2-tuple of digits, ignoring patch digit."""
        values_parts = tuple(int(v) for v in value.split("."))
        if len(values_parts) < 2:
            self.fail(
                f"{value!r} missing version parts. {self.example}",
                param,
                ctx,
            )
        major, minor, *patches = values_parts
        return major, minor


@click.group()
def djcodemod():
    """Automatically fix Django deprecations."""


@djcodemod.command()
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    required=True,
)
@click.option(
    "--removed-in",
    "removed_in",
    help="The version of Django where feature are removed.",
    type=VersionParamType(REMOVED_IN),
    multiple=True,
)
@click.option(
    "--deprecated-in",
    "deprecated_in",
    help="The version of Django where deprecations started.",
    type=VersionParamType(DEPRECATED_IN),
    multiple=True,
)
@click.option(
    "--codemod",
    "codemod",
    help="Choose a specific codemod to run. Can be repeated.",
    type=CodemodChoice(list(BY_NAME.keys())),
    multiple=True,
)
def run(
    removed_in: List[Tuple[int, int]],
    deprecated_in: List[Tuple[int, int]],
    codemod: List[str],
    src: Tuple[str, ...],
) -> None:
    """
    Automatically fixes deprecations removed Django deprecations.

    This command takes the path to target as argument and a version of
    Django to select code modifications to apply.
    """
    codemodders_set = set()
    for version in removed_in:
        codemodders_set |= set(REMOVED_IN[version])
    for version in deprecated_in:
        codemodders_set |= set(DEPRECATED_IN[version])
    for name in codemod:
        codemodders_set.add(BY_NAME[name])
    if not codemodders_set:
        raise click.UsageError(
            "No codemods were selected. "
            "Specify '--removed-in' and/or '--deprecated-in' and/or '--codemod'."
        )
    codemodders_list = sorted(codemodders_set, key=lambda m: m.__name__)
    click.echo(f"Running codemods: {', '.join(m.__name__ for m in codemodders_list)}")
    command_instance = BaseCodemodCommand(codemodders_list, CodemodContext())
    files = get_sources(src)
    call_command(command_instance, files)


def call_command(command_instance: BaseCodemodCommand, files: List[Path]):
    """Call libCST with our customized command."""
    try:
        # Super simplified call
        result = parallel_exec_transform_with_prettyprint(
            command_instance,
            files,  # type: ignore
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


@djcodemod.command("list")
def list_() -> None:
    """Print all available codemodders as a table."""
    console = Console()
    table = Table(show_header=True, header_style="bold")
    # Headers
    table.add_column("Codemodder")
    table.add_column("Deprecated in", justify="right")
    table.add_column("Removed in", justify="right")
    table.add_column("Description")
    # Content
    prev_version = None
    for name, deprecated_in, removed_in, description in generate_rows():
        if prev_version and prev_version != (deprecated_in, removed_in):
            table.add_row()
        table.add_row(name, deprecated_in, removed_in, Markdown(description))
        prev_version = (deprecated_in, removed_in)
    # Print it out
    console.print(table)


def generate_rows() -> Generator[Tuple[str, str, str, str], None, None]:
    """Build up the rows for the table of codemodders."""
    codemodders_list = sorted(
        iter_codemodders(), key=lambda obj: (obj.deprecated_in, obj.removed_in)
    )
    for codemodder in codemodders_list:
        yield (
            codemodder.__name__,
            version_str(codemodder.deprecated_in),
            version_str(codemodder.removed_in),
            get_short_description(codemodder),
        )


def get_short_description(codemodder: Type[BaseDjCodemodTransformer]) -> str:
    """Get a one line description of the codemodder from its docstring."""
    if codemodder.__doc__ is None:
        return ""
    for line in codemodder.__doc__.split("\n"):
        description = line.strip()
        if description:
            return description
    return ""


def version_str(version_parts: Tuple[int, int]) -> str:
    """Format the version tuple as string."""
    return ".".join(str(d) for d in version_parts)
