# SauceDemo Test Automation Framework

A comprehensive test automation framework for SauceDemo e-commerce application using Python and Playwright.

## Overview

This project implements automated regression tests for [SauceDemo](https://www.saucedemo.com), covering critical user flows including authentication, shopping cart operations, and checkout processes.

## Technology Stack

- **Language**: Python 3.9+
- **Test Framework**: Playwright for Python
- **Test Runner**: pytest
- **Reporting**: pytest-html
- **CI/CD**: GitHub Actions

### Why Playwright?

Playwright was chosen for this project because:
- **Modern & Reliable**: Built-in auto-waiting eliminates flaky tests
- **Fast Execution**: Parallel test execution support
- **Cross-browser**: Supports Chromium, Firefox, and WebKit
- **Excellent API**: Intuitive Python API with great documentation
- **Network Control**: Built-in request interception and mocking capabilities
- **Debugging**: Rich debugging tools (trace viewer, screenshots, videos)

## Project Structure

```
assessment-swag-labs/
├── tests/                    # Test suites
│   ├── test_login.py         # Authentication tests
│   ├── test_cart.py          # Shopping cart tests
│   ├── test_checkout.py      # Checkout flow tests
│   └── conftest.py           # Pytest fixtures and configuration
├── pages/                    # Page Object Model classes
│   ├── login_page.py         # Login page interactions
│   ├── inventory_page.py     # Product listing page
│   ├── cart_page.py          # Shopping cart page
│   └── checkout_page.py      # Checkout pages
├── utils/                     # Utility functions
│   ├── config.py             # Configuration management
│   └── helpers.py            # Helper functions
├── data/                      # Test data
│   └── test_data.json        # Test data in JSON format
├── reports/                   # Test reports (generated)
├── .github/
│   └── workflows/
│       └── tests.yml         # GitHub Actions CI workflow
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd assessment-swag-labs
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

6. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration if needed
   ```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Suites

```bash
# Run only login tests
pytest -m login

# Run only cart tests
pytest -m cart

# Run only checkout tests
pytest -m checkout
```

### Run Specific Test File

```bash
pytest tests/test_login.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run in Headed Mode (see browser)

```bash
pytest --headed
```

### Run with Screenshots on Failure

Screenshots are automatically captured on test failures and saved in `test-results/` directory.

## Test Coverage

### Authentication Tests (`test_login.py`)

- ✅ Valid login with correct credentials
- ✅ Invalid username
- ✅ Invalid password
- ✅ Locked out user handling
- ✅ Empty username validation
- ✅ Empty password validation
- ✅ Empty credentials validation
- ✅ Login page elements visibility

### Shopping Cart Tests (`test_cart.py`)

- ✅ Add single item to cart
- ✅ Add multiple items to cart
- ✅ Remove item from inventory page
- ✅ Remove item from cart page
- ✅ Cart persistence across navigation
- ✅ Cart badge count updates
- ✅ Cart items display correctly
- ✅ Proceed to checkout from cart

### Checkout Tests (`test_checkout.py`)

- ✅ Complete end-to-end checkout flow
- ✅ Checkout form validation (missing first name)
- ✅ Checkout form validation (missing last name)
- ✅ Checkout form validation (missing postal code)
- ✅ Cancel checkout functionality
- ✅ Logout after checkout
- ✅ Checkout with multiple items

## Page Object Model (POM)

The framework uses the Page Object Model pattern to improve maintainability and reduce code duplication:

- **LoginPage**: Handles all login page interactions
- **InventoryPage**: Manages product listing, sorting, and cart operations
- **CartPage**: Handles shopping cart operations
- **CheckoutPage**: Manages checkout information and completion

## Test Data Management

Test data is stored in `data/test_data.json` and includes:
- User credentials (standard, locked_out, problem, etc.)
- Customer information for checkout
- Product names

## Configuration

Configuration is managed through:
- `utils/config.py`: Base URLs, credentials, timeouts
- `.env` file: Environment-specific variables (optional)
- `pytest.ini`: Pytest configuration and markers

## Reporting

After test execution, HTML reports are generated in the `reports/` directory:
- `reports/report.html`: Comprehensive test report with results

Screenshots and videos are saved in `test-results/` directory on failures.

## CI/CD Integration

The project includes a GitHub Actions workflow (`.github/workflows/tests.yml`) that:
- Runs tests on push/PR to main/master/develop branches
- Installs dependencies and Playwright browsers
- Generates test reports
- Uploads test results as artifacts

## Best Practices Implemented

1. **Page Object Model**: Separates page interactions from test logic
2. **Fixtures**: Reusable test setup using pytest fixtures
3. **Data-Driven Testing**: Test data externalized in JSON files
4. **Robust Locators**: Using data-test attributes and role-based selectors
5. **Auto-waiting**: Leveraging Playwright's built-in waiting mechanisms
6. **Error Handling**: Comprehensive error messages and assertions
7. **Documentation**: Clear docstrings and README

## Troubleshooting

### Common Issues

1. **Browser not found**:
   ```bash
   playwright install
   ```

2. **Import errors**:
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **Tests timing out**:
   - Check network connectivity
   - Verify SauceDemo website is accessible
   - Increase timeout values in `utils/config.py` if needed

## Future Enhancements

Potential improvements for the framework:
- API testing integration
- Performance testing
- Visual regression testing
- Cross-browser testing matrix
- Test data generation utilities
- Allure reporting integration
- Docker containerization

## Author

Created as part of QA Engineer assessment for QTeam Solutions.

## License

This project is for assessment purposes.
