import os
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pathspec import PathSpec

from django_codemod.path_utils import (
    find_project_root,
    gen_python_files,
    get_gitignore,
    get_sources,
    normalize_path,
)

GIT_IGNORE_TEXT = """
__pycache__/
*.py[cod]
*$py.class
"""
IS_WIN = sys.platform.startswith("win")


@pytest.fixture()
def workspace():
    cwd = os.getcwd()
    with TemporaryDirectory() as temp_dir:
        try:
            ws = Path(temp_dir).resolve()
            os.chdir(ws)
            yield ws
        finally:
            os.chdir(cwd)


def test_get_sources(workspace):
    (workspace / ".git").mkdir()

    (workspace / "file1.py").touch()

    subdir1 = workspace / "subdir1"
    subdir1.mkdir()
    (subdir1 / "file2.py").touch()
    (subdir1 / "file3.py").touch()

    subdir2 = subdir1 / "subdir2"
    subdir2.mkdir()
    (subdir2 / "file4.py").touch()

    subdir3 = subdir1 / "subdir3"
    subdir3.mkdir()

    sources_list = get_sources(["file1.py", "."])

    assert sources_list == [
        Path("file1.py"),
        Path("subdir1/file2.py"),
        Path("subdir1/file3.py"),
        Path("subdir1/subdir2/file4.py"),
    ]


class TestFindProjectRoot:
    @pytest.mark.skipif(IS_WIN, reason="POSIX test")
    def test_basic(self, workspace):
        root_dir = find_project_root((".",))

        assert root_dir == Path("/")

    def test_git(self, workspace):
        (workspace / ".git").mkdir()

        root_dir = find_project_root((".",))

        assert root_dir == workspace

    def test_mercurial(self, workspace):
        (workspace / ".hg").mkdir()

        root_dir = find_project_root((".",))

        assert root_dir == workspace

    def test_pyproject_toml(self, workspace):
        (workspace / "pyproject.toml").touch()

        root_dir = find_project_root((".",))

        assert root_dir == workspace

    @pytest.mark.skipif(IS_WIN, reason="POSIX test")
    def test_empty_posix(self):
        root_dir = find_project_root([])
        assert root_dir == Path("/")

    @pytest.mark.skipif(not IS_WIN, reason="Windows test")
    def test_empty_windows(self):
        root_dir = find_project_root([])
        assert isinstance(root_dir, Path)
        assert re.match(r"[A-Z]:\\", str(root_dir))


def test_gitignore(workspace):
    (workspace / ".gitignore").write_text(GIT_IGNORE_TEXT)

    compiled_gitignore = get_gitignore(workspace)

    assert compiled_gitignore.match_file("example.py") is False
    assert compiled_gitignore.match_file("example.pyi") is False
    assert compiled_gitignore.match_file("example.txt") is False

    assert compiled_gitignore.match_file("example.pyc") is True
    assert compiled_gitignore.match_file("__pycache__/example.py") is True


class TestGenPythonPath:
    @pytest.fixture()
    def workspace_with_files(self, workspace):
        # non-python files: should be ignored
        (workspace / "file1.pyc").touch()
        (workspace / "file2.txt").touch()

        # Python file matching gitignore
        (workspace / "ignore1.py").touch()

        # file in root
        (workspace / "file1.py").touch()

        # subdir with files in it
        subdir1 = workspace / "subdir1"
        subdir1.mkdir()
        (subdir1 / "file2.py").touch()
        (subdir1 / "file3.py").touch()

        # nested subdir with files in it
        subdir2 = workspace / "subdir" / "subdir2"
        subdir2.mkdir(parents=True)
        (subdir2 / "file2.py").touch()
        (subdir2 / "file3.py").touch()

        yield workspace

    @pytest.fixture()
    def gitignore(self):
        return PathSpec.from_lines("gitwildmatch", ["ignore*.py"])

    @pytest.mark.parametrize(
        ("paths", "expected_set"),
        [
            (
                [Path(".")],
                {
                    Path("subdir/subdir2/file2.py"),
                    Path("subdir/subdir2/file3.py"),
                    Path("file1.py"),
                    Path("subdir1/file2.py"),
                    Path("subdir1/file3.py"),
                },
            ),
            (
                [Path("subdir")],
                {
                    Path("subdir/subdir2/file2.py"),
                    Path("subdir/subdir2/file3.py"),
                },
            ),
            (
                [Path("subdir"), Path("subdir1")],
                {
                    Path("subdir/subdir2/file2.py"),
                    Path("subdir/subdir2/file3.py"),
                    Path("subdir1/file2.py"),
                    Path("subdir1/file3.py"),
                },
            ),
        ],
    )
    def test_full(self, workspace_with_files, gitignore, paths, expected_set):
        files_iter = gen_python_files(paths, workspace_with_files, gitignore)
        assert set(files_iter) == expected_set

    def test_normalized_path_none(self, workspace_with_files, gitignore, mocker):
        mocker.patch("django_codemod.path_utils.normalize_path", lambda c, r: None)
        files_iter = gen_python_files([Path(".")], workspace_with_files, gitignore)
        assert set(files_iter) == set()


class TestNormalizePath:
    def test_basic(self, workspace):
        normalized_path = normalize_path(
            path=Path("example.py"),
            root=workspace,
        )

        assert normalized_path == "example.py"

    def test_subdirectory(self, workspace):
        normalized_path = normalize_path(
            path=Path("example/one/file1.py"),
            root=workspace,
        )

        assert normalized_path == "example/one/file1.py"

    def test_does_not_exist(self, workspace):
        normalized_path = normalize_path(
            path=Path("example.py"),
            root=workspace,
        )

        assert normalized_path == "example.py"

    def test_os_error(self, workspace, mocker):
        mocker.patch(
            "django_codemod.path_utils.Path.resolve",
            side_effect=OSError("something bad happened"),
        )
        normalized_path = normalize_path(
            path=Path("example.py"),
            root=workspace,
        )

        assert normalized_path is None

    @pytest.mark.skipif(IS_WIN, reason="POSIX-only test")
    def test_symlink(self, workspace):
        with TemporaryDirectory() as temp_dir:
            file = workspace / "example.py"
            file.symlink_to(Path(temp_dir) / "other.py")

            normalized_path = normalize_path(
                path=Path("example.py"),
                root=workspace,
            )

            assert normalized_path is None

    def test_value_error_not_swallowed(self, workspace, mocker):
        mocker.patch(
            "django_codemod.path_utils.Path.resolve",
            side_effect=ValueError("something bad happened"),
        )

        with pytest.raises(ValueError):
            normalize_path(
                path=Path("example.py"),
                root=workspace,
            )
