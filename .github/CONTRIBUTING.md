# Contributing Guide

Thank you for your interest in contributing to ifdo-py! This guide will help you
understand our contribution process and coding standards to ensure your
contributions can be efficiently integrated into the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Fork the Repository](#fork-the-repository)
  - [Clone Your Fork](#clone-your-fork)
  - [Set Up the Development Environment](#set-up-the-development-environment)
- [Development Workflow](#development-workflow)
  - [Create a Feature Branch](#create-a-feature-branch)
  - [Make Your Changes](#make-your-changes)
  - [Commit Your Changes](#commit-your-changes)
  - [Push Changes to Your Fork](#push-changes-to-your-fork)
  - [Create a Pull Request](#create-a-pull-request)
- [Code Standards](#code-standards)
  - [Code Style](#code-style)
  - [Type Hints](#type-hints)
  - [Documentation](#documentation)
  - [Testing](#testing)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Reporting](#issue-reporting)
- [License](#license)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Fork the Repository

Start by forking the [ifdo-py repository](https://github.com/csiro-fair/ifdo-py)
on GitHub:

1. Visit https://github.com/csiro-fair/ifdo-py
2. Click the "Fork" button in the top-right corner
3. Select your GitHub account as the destination for the fork

### Clone Your Fork

Once you have forked the repository, clone your fork to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/ifdo-py.git
cd ifdo-py
```

### Set Up the Development Environment

ifdo-py uses [UV](https://github.com/astral-sh/uv) for dependency management.
Follow these steps to set up your development environment:

1. Install UV if you haven't already
   ([Install Guide](https://docs.astral.sh/uv/getting-started/installation/)):
   ```bash
   pip install uv
   ```

2. Install project dependencies:
   ```bash
   # Creates a virtual environment .venv and installs dependencies
   uv sync --dev
   ```

3. Run the checks:
   ```bash
   # Run pre-commit hooks
   uv run pre-commit run --all-files

   # Run the test suite
   uv run pytest -c config/pytest.ini

   # Run the test suite across all supported Python versions
   uv run nox
   ```

## Development Workflow

### Create a Feature Branch

Before making changes, create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the purpose of your changes.

### Make Your Changes

Now you can make changes to the codebase. Be sure to follow our
[Code Standards](#code-standards). If your change tracks a new iFDO schema
version, also update the vendored schemas under `tests/schema/` so the test
suite validates against the version you are targeting.

### Commit Your Changes

When you're ready to commit your changes, stage and commit them:

```bash
git add .
git commit -m "Add a descriptive commit message"
```

Our pre-commit hooks will automatically run when you commit, ensuring your code
meets our standards.

### Push Changes to Your Fork

Push your changes to your fork on GitHub:

```bash
git push origin feature/your-feature-name
```

### Create a Pull Request

Once your changes are pushed to your fork, you can create a pull request:

1. Go to the
   [original ifdo-py repository](https://github.com/csiro-fair/ifdo-py)
2. Click "Pull Requests" and then "New Pull Request"
3. Click "compare across forks" and select your fork and branch
4. Click "Create Pull Request"
5. Provide a clear description of your changes and reference any related issues
6. Submit the pull request

## Code Standards

### Code Style

ifdo-py follows a strict code style to maintain consistency across the codebase:

- **Line Length**: Maximum line length is 120 characters
- **Python Version**: All code must be compatible with Python 3.10+
- **Formatting**: We use [Black](https://black.readthedocs.io/) for consistent
  code formatting
- **Linting**: We use [Ruff](https://github.com/astral-sh/ruff) for linting
  with our custom configuration

### Type Hints

ifdo-py uses type hints extensively to improve code quality and development
experience:

- All functions and methods should include type annotations
- Use modern union syntax (e.g., `X | Y` instead of `Union[X, Y]`)
- Function return types must be explicitly annotated
- Use built-in types like `dict`, `list` rather than imports from the `typing`
  module

### Documentation

Good documentation is essential:

- All modules, classes, methods, and functions should have docstrings following
  the
  [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Model fields should be documented in the class docstring's Attributes section
- Update the README when adding or changing user-facing functionality

### Testing

All code should be covered by tests:

- Write tests for new functionality, including round-trip serialization where
  relevant
- Ensure existing tests pass with your changes
- Tests live in the `tests/` directory and run with
  [pytest](https://docs.pytest.org/)
- Output written by the models is validated against the vendored iFDO JSON
  Schemas in `tests/schema/`; changes to serialization behaviour should keep
  that validation passing

## Pre-commit Hooks

ifdo-py uses pre-commit hooks to enforce code quality standards automatically:

1. **Ruff** - Linting with auto-fixes (configuration: `config/.ruff.toml`)
2. **Black** - Code formatting at 120 characters
3. **Mypy** - Static type checking (configuration: `config/mypy.ini`)
4. **Bandit** - Security linting at medium severity (configuration: `config/bandit.yml`)

The hooks run automatically when you commit. You can also run them manually:

```bash
# Run all hooks on all files
uv run pre-commit run --all-files

# Run a specific hook
uv run pre-commit run ruff --all-files
```

If a hook fails, fix the issues and try committing again.

## Pull Request Guidelines

To ensure your pull request is accepted:

1. **Follow the code standards** outlined in this document
2. **Write or update tests** for the changes you make
3. **Update documentation** if you're changing functionality
4. **Reference issues** in your pull request description
5. **Keep pull requests focused** - address one concern per PR
6. **Be responsive to feedback** during the review process

## Issue Reporting

If you find a bug or want to request a feature:

1. Check existing issues to avoid duplicates
2. Use the issue templates when available
3. Provide clear, detailed information about the issue or feature
4. Include steps to reproduce bugs when possible
5. Be responsive to questions about your issue

## License

By contributing to ifdo-py, you agree that your contributions will be licensed
under the project's [MIT License](../LICENSE).

---

Thank you for contributing to ifdo-py! Your efforts help improve this tool for
the marine imaging community.
