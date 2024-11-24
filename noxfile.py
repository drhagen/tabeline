from nox import options, parametrize
from nox_poetry import Session, session

options.sessions = ["test", "coverage", "lint"]


@session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def test(s: Session):
    s.install(".", "pytest", "pytest-cov")
    s.env["COVERAGE_FILE"] = f".coverage.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "tabeline")


@session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def test_pandas(s: Session):
    s.install(".[pandas]", "pytest", "pytest-cov")
    s.env["COVERAGE_FILE"] = f".coverage.pandas.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "tabeline", "tests/test_pandas_conversion.py")


@session(venv_backend="none")
def coverage(s: Session):
    s.run("coverage", "combine")
    s.run("coverage", "html")
    s.run("coverage", "xml")


@session(venv_backend="none")
@parametrize("command", [["ruff", "check", "."], ["ruff", "format", "--check", "."]])
def lint(s: Session, command: list[str]):
    s.run(*command)


@session(venv_backend="none")
def format(s: Session) -> None:
    s.run("ruff", "check", ".", "--select", "I", "--fix")
    s.run("ruff", "format", ".")
