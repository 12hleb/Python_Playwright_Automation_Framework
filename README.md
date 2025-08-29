# 🎭 Playwright UI/API Automation Framework

A modern, robust automation framework built with Python and Playwright for UI and API testing. This framework follows best practices and provides a solid foundation for test automation projects.

## 🚀 Features

### UI Testing
- **Page Object Model (POM)** - Clean, maintainable page objects
- **Cross-browser testing** - Chrome, Firefox, Safari, Edge
- **Mobile testing** - Responsive design validation
- **Visual testing** - Screenshot comparisons
- **Accessibility testing** - Basic accessibility checks

### API Testing
- **RESTful API testing** - Complete CRUD operations
- **Response validation** - JSON schema validation
- **Performance testing** - Response time assertions
- **Authentication support** - Token-based auth

### Framework Features
- **Parallel execution** - Fast test execution
- **Rich reporting** - HTML reports with screenshots
- **Allure integration** - Beautiful test reports
- **CI/CD ready** - GitHub Actions, Jenkins compatible
- **Environment management** - Multi-environment support
- **Logging** - Structured logging with Loguru

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd playwright-automation-framework
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers:**
```bash
playwright install
```

5. **Copy environment file:**
```bash
cp env.example .env
```

## 🏃‍♂️ Quick Start

### Run All Tests
```bash
pytest
```

### Run UI Tests Only
```bash
pytest -m ui
```

### Run API Tests Only
```bash
pytest -m api
```

### Run Smoke Tests
```bash
pytest -m smoke
```

### Run Tests in Parallel
```bash
pytest -n auto
```

### Run with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in Different Browsers
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run in Headed Mode (See Browser)
```bash
pytest --headed
```

## 📁 Project Structure

```
playwright-automation-framework/
├── api/                        # API clients and utilities
│   ├── __init__.py
│   ├── base_api.py            # Base API client
│   └── jsonplaceholder_api.py # Sample API client
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py            # Settings and configuration
├── pages/                      # Page Object Model
│   ├── __init__.py
│   ├── base_page.py           # Base page class
│   └── home_page.py           # Sample page object
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── api/                   # API tests
│   │   ├── __init__.py
│   │   └── test_jsonplaceholder.py
│   └── ui/                    # UI tests
│       ├── __init__.py
│       └── test_home_page.py
├── reports/                    # Test reports and artifacts
│   ├── screenshots/
│   ├── videos/
│   └── allure-results/
├── conftest.py                # Pytest configuration
├── pytest.ini                # Pytest settings
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Base URLs
BASE_URL=https://playwright.dev
API_BASE_URL=https://jsonplaceholder.typicode.com

# Browser Settings
BROWSER=chromium
HEADLESS=true
SLOW_MO=100

# Timeouts
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=30000

# Test Environment
ENVIRONMENT=test
```

### Pytest Configuration

Edit `pytest.ini` to customize test execution:

```ini
[tool:pytest]
markers =
    ui: UI tests using Playwright
    api: API tests
    smoke: Smoke tests
    regression: Regression tests
    slow: Slow running tests
```

## 📝 Writing Tests

### UI Test Example

```python
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage

@pytest.mark.ui
def test_home_page_loads(page: Page):
    """Test that the home page loads successfully."""
    home_page = HomePage(page)
    home_page.open()
    
    assert "Playwright" in home_page.get_title()
    assert home_page.is_logo_visible()
```

### API Test Example

```python
import pytest
from api.jsonplaceholder_api import JSONPlaceholderAPI

@pytest.mark.api
def test_get_posts(api_client):
    """Test getting all posts."""
    posts = api_client.get_posts()
    
    assert isinstance(posts, list)
    assert len(posts) > 0
```

### Page Object Example

```python
from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "#login"
    
    def login(self, username: str, password: str):
        self.fill_input(self.username_input, username)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)
```

## 📊 Test Reports

### HTML Reports
```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Reports
```bash
# Generate results
pytest --alluredir=reports/allure-results

# Serve report
allure serve reports/allure-results
```

## 🎯 Best Practices

### 1. Page Object Model
- Keep page objects simple and focused
- Use descriptive method names
- Return page objects for method chaining

### 2. Test Organization
- Use meaningful test names
- Group related tests in classes
- Use appropriate pytest markers

### 3. Assertions
- Use descriptive assertion messages
- Verify both positive and negative scenarios
- Test edge cases

### 4. Test Data
- Use factories for test data generation
- Keep test data separate from test logic
- Use fixtures for reusable test setup

### 5. Error Handling
- Take screenshots on failures
- Log important test steps
- Handle expected exceptions gracefully

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install
    - name: Run tests
      run: pytest --html=reports/report.html
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: reports/
```

## 🛠️ Useful Commands

```bash
# Run specific test file
pytest tests/ui/test_home_page.py

# Run with specific browser
pytest --browser firefox --headed

# Run with video recording
RECORD_VIDEOS=true pytest

# Run with debug mode
pytest -s -v

# Run failed tests only
pytest --lf

# Run tests matching pattern
pytest -k "test_login"

# Run with coverage
pytest --cov=.

# Dry run (collect tests only)
pytest --collect-only
```

## 🐛 Debugging

### Debug Mode
```bash
# Run in debug mode with visible browser
pytest --headed --slowmo=1000 -s

# Add breakpoints in code
import pdb; pdb.set_trace()
```

### Screenshots and Videos
- Screenshots are automatically taken on test failures
- Enable video recording with `RECORD_VIDEOS=true`
- Check `reports/screenshots/` and `reports/videos/`

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
- [API Testing Best Practices](https://playwright.dev/python/docs/api-testing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Testing! 🎭** 🎭 CI/CD Pipeline Active - Fri Aug 29 13:53:32 EDT 2025
