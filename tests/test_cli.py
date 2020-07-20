import click
import pytest
from click.testing import CliRunner
from libcst.codemod import ParallelTransformResult

from django_codemod import cli
from django_codemod.cli import DEPRECATED_IN, REMOVED_IN, build_command, call_command


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
    return build_command([])


def test_missing_argument(cli_runner):
    """Should explain missing arguments."""
    result = cli_runner.invoke(cli.djcodemod)

    assert result.exit_code == 2
    assert "Error: Missing argument 'PATH'" in result.output


@pytest.mark.parametrize(
    "command_line",
    [
        # Missing options
        ["."],
        # Too many options
        ["--removed-in", "3.0", "--deprecated-in", "2.0", "."],
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
    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "3", "."])

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
    result = cli_runner.invoke(cli.djcodemod, [option, version, "."])

    assert result.exit_code == 2
    assert f"'{version}' is not supported. Versions supported:" in result.output


def test_invalid_version(cli_runner):
    result = cli_runner.invoke(cli.djcodemod, ["--removed-in", "not.a.version", "."])

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
def test_basic_arguments(mocker, cli_runner, option, version):
    call_command = mocker.patch("django_codemod.cli.call_command")

    result = cli_runner.invoke(cli.djcodemod, [option, version, "."])

    assert result.exit_code == 0
    call_command.assert_called_once()


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
        (2, 1): ["InlineHasAddPermissionsTransformer"],
        (2, 0): [
            "AbsPathTransformer",
            "AvailableAttrsTransformer",
            "ContextDecoratorTransformer",
            "LRUCacheTransformer",
            "RenderToResponseTransformer",
            "UnicodeCompatibleTransformer",
        ],
        (1, 11): ["ModelsPermalinkTransformer"],
        (1, 10): ["URLResolversTransformer"],
        (1, 9): ["OnDeleteTransformer"],
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
        (3, 0): [
            "AbsPathTransformer",
            "AvailableAttrsTransformer",
            "ContextDecoratorTransformer",
            "InlineHasAddPermissionsTransformer",
            "LRUCacheTransformer",
            "RenderToResponseTransformer",
            "UnicodeCompatibleTransformer",
        ],
        (2, 1): ["ModelsPermalinkTransformer"],
        (2, 0): ["OnDeleteTransformer", "URLResolversTransformer"],
    }
