# Test Suite for Jira Spec Sheet Sync

This directory contains comprehensive tests for the Jira Spec Sheet Sync application.

## Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_data.py             # Mock data for testing
├── test_jira_client.py      # Tests for JIRA client functionality
├── test_spec_sheet_generator.py  # Tests for spec sheet generation
└── README.md               # This file
```

## Running Tests

### Quick Start

```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py --verbose

# Run with coverage report
python run_tests.py --coverage
```

### Via Menu System

1. Run `python start.py`
2. Select option `8. 🧪 Run Tests`
3. Choose your test configuration

### Advanced Usage

```bash
# Run only unit tests
python run_tests.py --unit

# Run specific test file
python run_tests.py --file test_jira_client.py

# Run tests matching a pattern
python run_tests.py --pattern "test_version"

# Install dependencies and run tests
python run_tests.py --install-deps --coverage
```

### Direct pytest Usage

```bash
# Basic test run
pytest tests/

# With coverage
pytest --cov=utils --cov=spec-sheet tests/

# Specific test class
pytest tests/test_jira_client.py::TestJiraClient

# Specific test method
pytest tests/test_jira_client.py::TestJiraClient::test_get_project_versions
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

- Test individual functions and methods
- Use mock data to isolate components
- Fast execution
- Focus on business logic

### Integration Tests (`@pytest.mark.integration`)

- Test component interactions
- Use real-like data flows
- Test end-to-end workflows
- Slower execution

## Test Data

All tests use consistent mock data defined in `test_data.py`:

- **Mock Epics**: 3 epics with different statuses and versions
- **Mock Stories**: 7 stories across epics with various risk profiles
- **Mock Versions**: 2 project versions (v2 released, v3 unreleased)
- **Mock Fields**: JIRA custom field definitions

## Key Test Areas

### JIRA Client (`test_jira_client.py`)

- ✅ API request handling
- ✅ Version filtering (fixed pagination bug)
- ✅ Epic and story retrieval
- ✅ Story points extraction
- ✅ Error handling
- ✅ Connection testing

### Spec Sheet Generator (`test_spec_sheet_generator.py`)

- ✅ Team member and team calculations
- ✅ Sprint planning estimates
- ✅ Risk profile determination
- ✅ Price calculations (proven/experimental/dependant)
- ✅ MoSCoW priority detection
- ✅ Spreadsheet structure validation
- ✅ Integration workflow testing

## Coverage Goals

The test suite aims for:

- **>90%** code coverage for core business logic
- **>80%** overall coverage
- **100%** coverage for critical calculation functions

## Mock Strategy

Tests use comprehensive mocking to:

- Avoid real JIRA API calls
- Ensure consistent test data
- Enable offline testing
- Speed up test execution
- Test error scenarios safely

## Adding New Tests

1. **Add test data** to `test_data.py` if needed
2. **Create test fixtures** in `conftest.py` for reusable setup
3. **Write focused tests** that test one thing at a time
4. **Use descriptive names** like `test_calculate_sprint_estimates_with_zero_velocity`
5. **Add markers** for test categorization (`@pytest.mark.unit`)

## Continuous Integration

The test suite is designed to run in CI/CD environments:

- No external dependencies during tests
- Deterministic results
- Clear pass/fail reporting
- Coverage reporting compatible with CI tools

## Troubleshooting

### Import Errors

- Ensure you're running from the project root
- Check that `PYTHONPATH` includes the project directory
- Verify all dependencies are installed

### Test Failures

- Check that mock data matches expected formats
- Verify environment variables are properly mocked
- Look for changes in business logic that need test updates

### Coverage Issues

- Run with `--coverage` to see detailed coverage report
- Check `htmlcov/index.html` for visual coverage report
- Focus on testing edge cases and error conditions
