import platform
import subprocess
from pathlib import Path

from nox import Session, options, parametrize
from nox_uv import session

options.default_venv_backend = "uv"
options.sessions = ["test", "test_polars", "test_pandas", "coverage", "lint"]


def _run_tests(s: Session, test_name: str, *pytest_args: str):
    # Almost all of this code is here to provide code coverage for the Rust
    # code, which requires instrumentation and post-processing

    # Set env so cargo-llvm-cov instruments the Rust build and writes profraw
    # files to its expected target dir.
    # This command spits out shell commmands to set variables, so they must be
    # parsed, somewhat fragilly.
    cov_env_output = subprocess.check_output(["cargo", "llvm-cov", "show-env"], text=True)
    for line in cov_env_output.splitlines():
        key, _, value = line.partition("=")
        s.env[key] = value.strip().strip("'")

    # Install Tabeline into the test virtual environment
    # This may seem like a weird way to install the current project, but this is
    # the only way to do it so that the Rust code actually builds and also does
    # not interfere with other environments.
    # Here are some simpler ways to build that do not work and why:
    # 1. Do not build with `uv sync` because that is an editable build and that
    #    won't build the Rust code.
    # 2. Do not build with `uv sync --no-editable` because that won't rebuild
    #    when the project is changed.
    # 3. Do not build with `maturin develop --uv` because that will cause the
    #    intrumentation to be left in dev environment causing raw coverage files
    #    to be left in working directories every time Python is invoked.
    s.run(
        "uv",
        "pip",
        "install",
        # Turn off build isolation so that we still get caching of Rust compiles
        "--no-build-isolation",
        # Force installation so that changes get installed
        "--reinstall-package",
        "tabeline",
        # We already installed dependencies with nox-uv
        "--no-deps",
        # `uv pip install` triggers a maturin release build, which will put the
        # instrumented binary in  target/release instead of target/debug where
        # `cargo llvm-cov report` expects it
        "--config-settings",
        "build-args=--profile=dev",
        ".",
    )

    coverage_data = f".coverage.{test_name}"

    # Run the tests with coverage
    s.run("coverage", "run", "--data-file", coverage_data, "-m", "pytest", *pytest_args)

    # Convert the Python coverage data to the common lcov format
    s.run("coverage", "lcov", "--data-file", coverage_data, "-o", f"python.{test_name}.lcov")
    Path(coverage_data).unlink()

    # Convert the Rust coverage data to the common lcov format
    # This must be done here because the cargo-llvm-cov data is not portable
    # (unlike the Python data)
    s.run(
        "cargo",
        "llvm-cov",
        "report",
        "--lcov",
        "--output-path",
        f"rust.{test_name}.lcov",
        "--ignore-filename-regex",
        r"/\.cargo/|/rustc/",
        external=True,
    )


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_no_install_project=True,
)
def test(s: Session):
    _run_tests(s, f"{platform.machine()}.{platform.system()}.{s.python}")


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_extras=["polars"],
    uv_no_install_project=True,
)
def test_polars(s: Session):
    _run_tests(
        s,
        f"{platform.machine()}.{platform.system()}.{s.python}.polars",
        "tests/test_polars.py",
    )


@session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    uv_extras=["pandas"],
    uv_no_install_project=True,
)
def test_pandas(s: Session):
    _run_tests(
        s,
        f"{platform.machine()}.{platform.system()}.{s.python}.pandas",
        "tests/test_pandas.py",
    )


@session(uv_only_groups=["test"])
def coverage(s: Session):
    lcovs = sorted(Path().glob("python.*.lcov")) + sorted(Path().glob("rust.*.lcov"))
    add_args = [arg for p in lcovs for arg in ("-a", str(p))]
    s.run("lcov", *add_args, "-o", "combined.lcov", external=True)
    s.run(
        "genhtml",
        "combined.lcov",
        "-o",
        "htmlcov",
        external=True,
    )


@session(uv_only_groups=["lint"])
@parametrize(
    "command",
    [
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
        ["cargo", "clippy", "--locked", "--", "-D", "warnings"],
        ["cargo", "fmt", "--check"],
    ],
)
def lint(s: Session, command: list[str]):
    s.run(*command, external=True)


@session(uv_only_groups=["lint"])
def format(s: Session):
    s.run("ruff", "check", ".", "--select", "I", "--select", "RUF022", "--fix")
    s.run("ruff", "format", ".")
    s.run("cargo", "fmt", external=True)
