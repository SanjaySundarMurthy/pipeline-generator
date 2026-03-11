# Contributing to pipeline-generator

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/SanjaySundarMurthy/pipeline-generator.git
cd pipeline-generator

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pipe-gen --version
```

## Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=pipeline_generator --cov-report=term-missing

# Run a specific test class
pytest tests/test_generator.py::TestGitHubActions -v
```

## Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .
```

## Adding a New Language

1. Add language tools config to `pipeline_generator/presets.py` in `LANGUAGE_TOOLS`
2. Add a preset to `PRESETS`
3. Add detection logic to `pipeline_generator/detector.py`
4. Add an example spec in `examples/`
5. Add tests in `tests/test_generator.py`
6. Update README.md

## Adding a New Platform

1. Create a new generator in `pipeline_generator/platforms/`
2. Inherit from `BasePlatform` and implement all abstract methods
3. Register it in `pipeline_generator/generator.py` `PLATFORMS` dict
4. Add platform choice to CLI in `pipeline_generator/cli.py`
5. Add tests
6. Update README.md

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Write tests for your changes
4. Ensure all tests pass: `pytest -v`
5. Lint your code: `ruff check .`
6. Commit with a clear message
7. Push and create a Pull Request

## Reporting Issues

When reporting bugs, please include:
- Python version (`python --version`)
- OS (Windows/macOS/Linux)
- Full error output
- Your pipeline.yaml spec (if applicable)
