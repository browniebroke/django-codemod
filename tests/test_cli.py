import pytest
from click.testing import CliRunner

from django_codemod import cli
from django_codemod.commands.base import BaseCodemodCommand


@pytest.fixture()
def cli_runner():
    return CliRunner()


def test_missing_argument(cli_runner):
    """Should explain missing arguments."""
    result = cli_runner.invoke(cli.djcodemod)

    assert result.exit_code == 2
    assert "Error: Missing argument 'PATH'" in result.output


def test_missing_option(cli_runner):
    """Should explain missing option."""
    result = cli_runner.invoke(cli.djcodemod, ["."])

    assert result.exit_code == 2
    assert "Error: Missing option '--removed-in'." in result.output


def test_help(cli_runner):
    """The --help option should be available."""
    help_result = cli_runner.invoke(cli.djcodemod, ["--help"])

    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output


def test_missing_version_parts(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "3", "."])

    assert result.exit_code == 2
    assert "missing version parts." in result.output


def test_non_supported_version(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "1.0", "."])

    assert result.exit_code == 2
    assert "'1.0' is not supported. Versions supported:" in result.output


def test_invalid_version(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "not.a.version", "."])

    assert result.exit_code == 2
    assert "'not.a.version' is not a valid version" in result.output


def test_basic_arguments(mocker, cli_runner):
    call_command = mocker.patch("django_codemod.cli.call_command")

    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "3.0", "."])

    assert result.exit_code == 0
    call_command.assert_called_once()
    assert len(call_command.call_args.args) == 2
    cmd_arg, path_arg = call_command.call_args.args
    assert isinstance(cmd_arg, BaseCodemodCommand)
    assert path_arg == "."
