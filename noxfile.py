from __future__ import annotations

import platform

from nox import Session, options, parametrize, session

options.sessions = ["test", "test_polars", "test_pandas", "coverage", "lint"]


def _install_test_environment(s: Session, extras: list[str]):
    extras = [f"--extra={extra}" for extra in extras]

    if "--use-dist" in s.posargs:
        s.run_install(
            "uv",
            "sync",
            f"--python={s.virtualenv.location}",
            "--no-default-groups",
            "--group=test",
            *extras,
            "--no-install-project",
            env={"UV_PROJECT_ENVIRONMENT": s.virtualenv.location},
        )
        s.run_install(
            "uv",
            "pip",
            "install",
            f"--python={s.virtualenv.location}",
            "--no-index",
            "--find-links=dist/",
            "--no-deps",
            "tabeline",
            env={"UV_PROJECT_ENVIRONMENT": s.virtualenv.location},
        )
    else:
        s.run_install(
            "uv",
            "sync",
            f"--python={s.virtualenv.location}",
            "--no-default-groups",
            "--group=test",
            *extras,
            env={"UV_PROJECT_ENVIRONMENT": s.virtualenv.location},
        )


def _install_group_environment(s: Session, group: str):
    s.run_install(
        "uv",
        "sync",
        f"--python={s.virtualenv.location}",
        f"--only-group={group}",
        env={"UV_PROJECT_ENVIRONMENT": s.virtualenv.location},
    )


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test(s: Session):
    _install_test_environment(s, extras=[])

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest")


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test_polars(s: Session):
    _install_test_environment(s, extras=["polars"])

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}.polars"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest", "tests/test_polars.py")


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test_pandas(s: Session):
    _install_test_environment(s, extras=["pandas"])

    coverage_file = f".coverage.{platform.machine()}.{platform.system()}.{s.python}.pandas"
    s.run("coverage", "run", "--data-file", coverage_file, "-m", "pytest", "tests/test_pandas.py")


@session()
def coverage(s: Session):
    _install_group_environment(s, "test")

    s.run("coverage", "combine")
    s.run("coverage", "html")
    s.run("coverage", "xml")


@session()
@parametrize(
    "command",
    [
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
        ["cargo", "clippy", "--locked", "--", "-D", "warnings"],
    ],
)
def lint(s: Session, command: list[str]):
    _install_group_environment(s, "lint")

    s.run(*command, external=True)


@session()
def format(s: Session):
    _install_group_environment(s, "lint")

    s.run("ruff", "check", ".", "--select", "I", "--select", "RUF022", "--fix")
    s.run("ruff", "format", ".")
    s.run("cargo", "fmt", external=True)
