# Contributing

Tabeline is free and open source software developed under an MIT license. Development occurs at the [GitHub project](https://github.com/drhagen/tabeline). Contributions, big and small, are welcome.

Bug reports and feature requests may be made directly on the [issues](https://github.com/drhagen/tabeline/issues) tab.

To make a pull request, you will need to fork the repo, clone the repo, make the changes, run the tests, push the changes, and [open a PR](https://github.com/drhagen/tabeline/pulls).

## Cloning the repo

To make a local copy of Tabeline, clone the repository with git:

```shell
git clone https://github.com/drhagen/tabeline.git
```

## Installing from source

Tabeline uses Poetry as its packaging and dependency manager. In whatever Python environment you prefer, [install Poetry](https://python-poetry.org/docs/) and then use Poetry to install Tabeline and its dependencies:

```shell
pip install poetry
poetry install
```

## Testing

Tabeline uses pytest to run the tests in the `tests/` directory. The test command is encapsulated with Nox:

```shell
poetry run nox -s test test_pandas
```

This will try to test with all compatible Python versions that `nox` can find. To run the tests with only a particular version, run something like this:

```shell
poetry run nox -s test-3.9 test_pandas-3.9
```

It is good to run the tests locally before making a PR, but it is not necessary to have all Python versions run. It is rare for a failure to appear in a single version, and the CI will catch it anyway. 

## Code quality

Tabeline uses Black, isort, and Flake8 to ensure a minimum standard of code quality. The code quality commands are encapsulated with Nox:

```shell
poetry run nox -s black
poetry run nox -s isort
poetry run nox -s flake8
```

## Generating the docs

Tabeline uses MkDocs to generate HTML docs from Markdown. For development purposes, they can be served locally without needing to build them first:

```shell
poetry run mkdocs serve
```

To deploy the current docs to GitHub Pages, Tabeline uses the MkDocs `gh-deploy` command that builds the static site on the `gh-pages` branch, commits, and pushes to the origin:

```shell
poetry run mkdocs gh-deploy
```

## Making a release

1. Bump
    1. Increment version in `pyproject.toml`
    2. Commit with message "Bump version number to X.Y.Z"
    3. Push commit to GitHub
    4. Check GitHub Actions to ensure all tests pass
2. Tag
    1. Tag commit with "vX.Y.Z"
    2. Push commit to GitHub
    3. Check GitHub Actions for tag
3. Build
    1. Clear `dist/`
    2. Run `poetry build`
    3. Verify that sdist (`.tar.gz`) and bdist (`.whl`) are in `dist/`
4. Publish
    1. Run `poetry publish -r test`
    2. Check [PyPI test server](https://test.pypi.org/project/tabeline/) for good upload
    3. Run `poetry publish`
    4. Check [PyPI](https://pypi.org/project/tabeline/) for good upload
5. Document
    1. Create [GitHub release](https://github.com/drhagen/tabeline/releases) with name "Tabeline X.Y.Z" and major changes in body
    2. If appropriate, deploy updated docs
