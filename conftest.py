"""
Global pytest configuration and fixtures for Playwright automation framework.
"""

import pytest
import os
from typing import Generator
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from loguru import logger
from config.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load test settings."""
    return Settings()


@pytest.fixture(scope="session")
def browser_context_args(browser_name: str) -> dict:
    """Configure browser context arguments."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "reports/videos/" if os.getenv("RECORD_VIDEO") == "true" else None,
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new page for each test."""
    page = context.new_page()
    logger.info(f"Created new page: {page.url}")
    
    yield page
    
    logger.info(f"Closing page: {page.url}")
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page, settings: Settings) -> Page:
    """Create an authenticated page (example for login)."""
    # This is an example - implement your authentication logic
    page.goto(settings.base_url)
    return page


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create reports directory
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("reports/traces", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    
    logger.info("Playwright automation framework initialized")


def pytest_runtest_makereport(item, call):
    """Create test reports and handle failures."""
    if call.when == "call":
        if call.excinfo is not None and "page" in item.fixturenames:
            page = item.funcargs["page"]
            screenshot_name = f"screenshots/{item.name}_{call.when}.png"
            page.screenshot(path=f"reports/{screenshot_name}")
            logger.error(f"Test failed, screenshot saved: {screenshot_name}")


@pytest.fixture(autouse=True)
def setup_test_environment(request):
    """Setup test environment before each test."""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    yield
    
    logger.info(f"Finished test: {test_name}")


# Custom markers for better test organization
pytest_plugins = ["pytest_html"] 