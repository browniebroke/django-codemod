from pathlib import Path

import click
import pytest
from click.testing import CliRunner
from libcst.codemod import CodemodContext, ParallelTransformResult

from django_codemod import cli
from django_codemod.cli import (
    DEPRECATED_IN,
    REMOVED_IN,
    call_command,
    get_short_description,
)
from django_codemod.commands import BaseCodemodCommand


@pytest.fixture()
def cli_runner():
    return CliRunner()


@pytest.fixture()
def gather_files_mocked(mocker):
    """Mock return value of gather_files from libCST."""
    gather_files = mocker.patch("django_codemod.cli.gather_files")
    gather_files.return_value = ["some/file.py"]


@pytest.fixture()
def command_instance():
    """Dummy command instance to test call_command."""
    return BaseCodemodCommand([], CodemodContext())


def test_missing_argument(cli_runner):
    """Should explain missing arguments."""
    result = cli_runner.invoke(cli.djcodemod, ["run"])

    assert result.exit_code == 2
    assert "Error: Missing argument 'PATH'" in result.output


@pytest.mark.parametrize(
    "command_line",
    [
        # Missing options
        ["run", "."],
        # Too many options
        ["run", "--removed-in", "3.0", "--deprecated-in", "2.0", "."],
    ],
)
def test_invalid_options(cli_runner, command_line):
    """Should explain missing option."""
    result = cli_runner.invoke(cli.djcodemod, command_line)

    assert result.exit_code == 2
    assert (
        "Error: You must specify either '--removed-in' or "
        "'--deprecated-in' but not both." in result.output
    )


def test_help(cli_runner):
    """The --help option should be available."""
    help_result = cli_runner.invoke(cli.djcodemod, ["--help"])

    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output


def test_missing_version_parts(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["run", "--removed-in", "3", "."])

    assert result.exit_code == 2
    assert "missing version parts." in result.output


@pytest.mark.parametrize(
    ("option", "version"),
    [
        # Removed in option
        ("--removed-in", "1.0"),
        ("--removed-in", "11.0"),
        # Deprecated in option
        ("--deprecated-in", "1.0"),
        ("--deprecated-in", "3.4"),
    ],
)
def test_non_supported_version(cli_runner, option, version):
    result = cli_runner.invoke(cli.djcodemod, ["run", option, version, "."])

    assert result.exit_code == 2
    assert f"'{version}' is not supported. Versions supported:" in result.output


def test_invalid_version(cli_runner):
    result = cli_runner.invoke(
        cli.djcodemod, ["run", "--removed-in", "not.a.version", "."]
    )

    assert result.exit_code == 2
    assert "'not.a.version' is not a valid version" in result.output


@pytest.mark.parametrize(
    ("option", "version"),
    [
        # Removed in option
        ("--removed-in", "3.0"),
        ("--deprecated-in", "2.0"),
    ],
)
@pytest.mark.parametrize("path", [".", "my_app"])
def test_basic_arguments(cli_runner, option, version, path):
    with cli_runner.isolated_filesystem() as tempdir:
        dir = Path(tempdir) / "my_app"
        dir.mkdir()
        for file_name in ["hello1.py", "hello2.py", "hello3.py"]:
            py_file = dir / file_name
            with py_file.open("w") as f:
                f.write('print("Hello World!")')

        result = cli_runner.invoke(cli.djcodemod, ["run", option, version, path])

    assert result.exit_code == 0, result
    assert "Finished codemodding 3 files!" in result.output


@pytest.mark.usefixtures("gather_files_mocked")
def test_call_command_success(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint"
    )
    executor.return_value = ParallelTransformResult(
        successes=1, failures=0, warnings=0, skips=0
    )

    result = call_command(command_instance, ".")

    assert result is None


@pytest.mark.usefixtures("gather_files_mocked")
def test_call_command_failure(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint"
    )
    executor.return_value = ParallelTransformResult(
        successes=0, failures=1, warnings=0, skips=0
    )

    with pytest.raises(click.exceptions.Exit):
        call_command(command_instance, ".")


@pytest.mark.usefixtures("gather_files_mocked")
def test_call_command_interrupted(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint",
        side_effect=KeyboardInterrupt(),
    )
    executor.return_value = ParallelTransformResult(
        successes=1, failures=0, warnings=0, skips=0
    )

    with pytest.raises(click.Abort):
        call_command(command_instance, ".")


def _mapping_repr(mapping):
    """Helper to return class names in the dict values."""
    return {
        version: [klass.__name__ for klass in classes_list]
        for version, classes_list in mapping.items()
    }


def test_deprecated_in_mapping():
    """Transformers found by the ``DEPRECATED_IN`` mapping."""
    assert _mapping_repr(DEPRECATED_IN) == {
        (3, 0): [
            "ForceTextTransformer",
            "HttpUrlQuotePlusTransformer",
            "HttpUrlQuoteTransformer",
            "HttpUrlUnQuotePlusTransformer",
            "HttpUrlUnQuoteTransformer",
            "IsSafeUrlTransformer",
            "SmartTextTransformer",
            "UGetTextLazyTransformer",
            "UGetTextNoopTransformer",
            "UGetTextTransformer",
            "UNGetTextLazyTransformer",
            "UNGetTextTransformer",
            "URLTransformer",
            "UnescapeEntitiesTransformer",
        ],
        (2, 2): [
            "FixedOffsetTransformer",
            "FloatRangeFormFieldTransformer",
            "FloatRangeModelFieldTransformer",
            "QuerySetPaginatorTransformer",
        ],
        (2, 1): [
            "InlineHasAddPermissionsTransformer",
        ],
        (2, 0): [
            "AbsPathTransformer",
            "AvailableAttrsTransformer",
            "ContextDecoratorTransformer",
            "HttpRequestXReadLinesTransformer",
            "LRUCacheTransformer",
            "RenderToResponseTransformer",
            "UnicodeCompatibleTransformer",
        ],
        (1, 11): [
            "ModelsPermalinkTransformer",
        ],
        (1, 10): [
            "URLResolversTransformer",
        ],
        (1, 9): [
            "AssignmentTagTransformer",
            "OnDeleteTransformer",
            "SignalDisconnectWeakTransformer",
        ],
    }


def test_removed_in_mapping():
    """Transformers found by the ``REMOVED_IN`` mapping."""
    assert _mapping_repr(REMOVED_IN) == {
        (4, 0): [
            "ForceTextTransformer",
            "HttpUrlQuotePlusTransformer",
            "HttpUrlQuoteTransformer",
            "HttpUrlUnQuotePlusTransformer",
            "HttpUrlUnQuoteTransformer",
            "IsSafeUrlTransformer",
            "SmartTextTransformer",
            "UGetTextLazyTransformer",
            "UGetTextNoopTransformer",
            "UGetTextTransformer",
            "UNGetTextLazyTransformer",
            "UNGetTextTransformer",
            "URLTransformer",
            "UnescapeEntitiesTransformer",
        ],
        (3, 1): [
            "FixedOffsetTransformer",
            "FloatRangeFormFieldTransformer",
            "FloatRangeModelFieldTransformer",
            "QuerySetPaginatorTransformer",
        ],
        (3, 0): [
            "AbsPathTransformer",
            "AvailableAttrsTransformer",
            "ContextDecoratorTransformer",
            "HttpRequestXReadLinesTransformer",
            "InlineHasAddPermissionsTransformer",
            "LRUCacheTransformer",
            "RenderToResponseTransformer",
            "UnicodeCompatibleTransformer",
        ],
        (2, 1): [
            "ModelsPermalinkTransformer",
        ],
        (2, 0): [
            "AssignmentTagTransformer",
            "OnDeleteTransformer",
            "SignalDisconnectWeakTransformer",
            "URLResolversTransformer",
        ],
    }


def test_list_command(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["list"])

    assert result.exit_code == 0, result
    assert "Codemodder" in result.output
    assert "Deprecated in" in result.output
    assert "Removed in" in result.output
    assert "Description" in result.output


class NoDocString:
    pass


class SingleLine:
    """This is the description."""


class MultiLine1:
    """This is the title.

    This is more details."""


class MultiLine2:
    """
    Another title.

    And even more extra stuff.
    """


@pytest.mark.parametrize(
    ("klass", "expected_result"),
    [
        (NoDocString, ""),
        (SingleLine, "This is the description."),
        (MultiLine1, "This is the title."),
        (MultiLine2, "Another title."),
    ],
)
def test_get_short_description(klass, expected_result):
    assert get_short_description(klass) == expected_result
