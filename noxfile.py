import platform

from nox import Session, options, parametrize
from nox_uv import session

options.default_venv_backend = "uv"
options.sessions = ["test", "test_polars", "test_pandas", "coverage", "lint"]


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_no_install_project=True,
)
def test(s: Session):
    if "--use-dist" in s.posargs:
        s.run(
            "uv",
            "pip",
            "install",
            "--reinstall-package=tabeline",
            "--no-index",
            "--find-links=dist/",
            "--no-deps",
            "tabeline",
        )
    else:
        s.run("uv", "pip", "install", "--no-deps", "-e", ".")

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest")


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_extras=["polars"],
    uv_no_install_project=True,
)
def test_polars(s: Session):
    if "--use-dist" in s.posargs:
        s.run(
            "uv",
            "pip",
            "install",
            "--reinstall-package=tabeline",
            "--no-index",
            "--find-links=dist/",
            "--no-deps",
            "tabeline",
        )
    else:
        s.run("uv", "pip", "install", "--no-deps", "-e", ".")

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}.polars"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest", "tests/test_polars.py")


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_extras=["pandas"],
    uv_no_install_project=True,
)
def test_pandas(s: Session):
    if "--use-dist" in s.posargs:
        s.run(
            "uv",
            "pip",
            "install",
            "--reinstall-package=tabeline",
            "--no-index",
            "--find-links=dist/",
            "--no-deps",
            "tabeline",
        )
    else:
        s.run("uv", "pip", "install", "--no-deps", "-e", ".")

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}.pandas"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest", "tests/test_pandas.py")


@session(uv_only_groups=["test"])
def coverage(s: Session):
    s.run("coverage", "combine")
    s.run("coverage", "html")
    s.run("coverage", "xml")


@session(uv_only_groups=["lint"])
@parametrize(
    "command",
    [
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
        ["cargo", "clippy", "--locked", "--", "-D", "warnings"],
    ],
)
def lint(s: Session, command: list[str]):
    s.run(*command, external=True)


@session(uv_only_groups=["lint"])
def format(s: Session):
    s.run("ruff", "check", ".", "--select", "I", "--select", "RUF022", "--fix")
    s.run("ruff", "format", ".")
    s.run("cargo", "fmt", external=True)
