from pathlib import Path

import click
import pytest
from click.testing import CliRunner
from libcst.codemod import CodemodContext, ParallelTransformResult

from django_codemod import cli, visitors
from django_codemod.commands import BaseCodemodCommand


@pytest.fixture()
def cli_runner():
    return CliRunner()


@pytest.fixture()
def get_sources_mocked(mocker):
    """Mock return value of get_sources util function."""
    gather_files = mocker.patch("django_codemod.cli.get_sources")
    gather_files.return_value = ["some/file.py"]


@pytest.fixture()
def command_instance():
    """Dummy command instance to test call_command."""
    return BaseCodemodCommand([], CodemodContext())


def test_missing_argument(cli_runner):
    """Should explain missing arguments."""
    result = cli_runner.invoke(cli.djcodemod, ["run"])

    assert result.exit_code == 2
    assert "Error" in result.output
    assert "Missing argument" in result.output


def test_no_mods_selected(cli_runner):
    """Should explain missing option."""
    result = cli_runner.invoke(cli.djcodemod, ["run", "."])

    assert result.exit_code == 2
    assert "No codemods were selected" in result.output


def test_help(cli_runner):
    """The --help option should be available."""
    help_result = cli_runner.invoke(cli.djcodemod, ["--help"])

    assert help_result.exit_code == 0
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
    assert "Invalid value for" in result.output
    assert "is not supported." in result.output
    assert "supported:" in result.output


def test_invalid_version(cli_runner):
    result = cli_runner.invoke(
        cli.djcodemod, ["run", "--removed-in", "not.a.version", "."]
    )

    assert result.exit_code == 2
    assert "'not.a.version' is not a valid version" in result.output


def test_run_help(cli_runner):
    result = cli_runner.invoke(
        cli.djcodemod,
        ["run", "--help"],
    )

    assert result.exit_code == 0
    assert "djcodemod list" in result.output


@pytest.mark.parametrize(
    ("option", "version"),
    [
        ("--removed-in", "3.0"),
        ("--deprecated-in", "2.0"),
        ("--codemod", "URLResolversTransformer"),
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


@pytest.mark.usefixtures("get_sources_mocked")
def test_call_command_success(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint"
    )
    executor.return_value = ParallelTransformResult(
        successes=1, failures=0, warnings=0, skips=0
    )

    result = cli.call_command(command_instance, ".")

    assert result is None


@pytest.mark.usefixtures("get_sources_mocked")
def test_call_command_failure(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint"
    )
    executor.return_value = ParallelTransformResult(
        successes=0, failures=1, warnings=0, skips=0
    )

    with pytest.raises(click.exceptions.Exit):
        cli.call_command(command_instance, ".")


@pytest.mark.usefixtures("get_sources_mocked")
def test_call_command_interrupted(command_instance, mocker):
    executor = mocker.patch(
        "django_codemod.cli.parallel_exec_transform_with_prettyprint",
        side_effect=KeyboardInterrupt(),
    )
    executor.return_value = ParallelTransformResult(
        successes=1, failures=0, warnings=0, skips=0
    )

    with pytest.raises(click.Abort):
        cli.call_command(command_instance, ".")


def _verify_mapping(mapping, version_attr):
    seen_names = set()
    for version, classes in mapping.items():
        seen_names |= {cls.__name__ for cls in classes}
        for cls in classes:
            # Verify we gathered the mapping correctly by version
            assert getattr(cls, version_attr) == version

    # Verify all codemods exported from visitors are mapped
    assert seen_names == set(visitors.__all__)


def test_deprecated_in_mapping():
    _verify_mapping(cli.DEPRECATED_IN, "deprecated_in")


def test_removed_in_mapping():
    _verify_mapping(cli.REMOVED_IN, "removed_in")


def test_list_command(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["list"])

    assert result.exit_code == 0, result
    assert "Codemodder" in result.output
    assert "Deprecated in" in result.output
    assert "Removed in" in result.output
    assert "Description" in result.output


class NoDocString:
    pass


class EmptyDocString:
    """"""  # noqa D419

    pass


class SingleLine:
    """The description."""


class MultiLine1:
    """
    Some title.

    This is more details.
    """


class MultiLine2:
    """
    Another title.

    And even more extra stuff.
    """


@pytest.mark.parametrize(
    ("klass", "expected_result"),
    [
        (NoDocString, ""),
        (EmptyDocString, ""),
        (SingleLine, "The description."),
        (MultiLine1, "Some title."),
        (MultiLine2, "Another title."),
    ],
)
def test_get_short_description(klass, expected_result):
    assert cli.get_short_description(klass) == expected_result
