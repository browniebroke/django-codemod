"""Some utilities to deal with files.

Inspired or taken from black:
https://github.com/psf/black
"""
from pathlib import Path
from typing import Iterable, Iterator, List, Optional

from pathspec import PathSpec


def get_sources(src: Iterable[str]) -> List[Path]:
    """Return a list of sources to codemod.

    Based on a list of paths or files, recursively find python source files,
    ignoring the ones according to `.gitignore`.
    """
    root = find_project_root(src)
    gitignore = get_gitignore(root)
    sources = set()
    for s in src:
        p = Path(s)
        paths = None
        if p.is_file():
            paths = [p]
        elif p.is_dir():
            paths = p.iterdir()
        if paths:
            sources.update(gen_python_files(paths, root, gitignore))
    return sorted(sources)


def find_project_root(sources: Iterable[str]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `sources`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not sources:
        return Path("/").resolve()

    path_srcs = [Path(Path.cwd(), src).resolve() for src in sources]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def get_gitignore(root: Path) -> PathSpec:
    """Return a PathSpec matching gitignore content if present."""
    gitignore = root / ".gitignore"
    lines: List[str] = []
    if gitignore.is_file():
        with gitignore.open() as gf:
            lines = gf.readlines()
    return PathSpec.from_lines("gitwildmatch", lines)


def gen_python_files(
    paths: Iterable[Path],
    root: Path,
    gitignore: PathSpec,
) -> Iterator[Path]:
    """Generate all files under `paths`.

    Files listed in .gitignore are not considered.
    """
    for child in paths:
        normalized_path = normalize_path(child, root)
        if normalized_path is None:
            continue

        # First ignore files matching .gitignore
        if gitignore.match_file(normalized_path):
            continue

        if child.is_dir():
            yield from gen_python_files(
                child.iterdir(),
                root,
                gitignore,
            )

        elif child.is_file() and str(child).endswith(".py"):
            yield child


def normalize_path(path: Path, root: Path) -> Optional[str]:
    """Normalize `path`. May return `None` if `path` was ignored."""
    try:
        abspath = path if path.is_absolute() else Path.cwd() / path
        normalized_path = abspath.resolve().relative_to(root).as_posix()
    except OSError as exc:
        print(f"{path} cannot be read because {exc}")
        return None
    except ValueError:
        if path.is_symlink():
            print(f"{path} is a symbolic link that points outside {root}")
            return None
        raise

    return normalized_path
