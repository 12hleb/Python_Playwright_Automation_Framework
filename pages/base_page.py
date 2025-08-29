"""
Base page class for Page Object Model implementation.
"""

from abc import ABC
from typing import Optional
from playwright.sync_api import Page, Locator
from loguru import logger


class BasePage(ABC):
    """Base page class that all page objects should inherit from."""
    
    def __init__(self, page: Page):
        """Initialize base page."""
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout
        
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL."""
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        
    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()
        
    def get_url(self) -> str:
        """Get current page URL."""
        return self.page.url
        
    def wait_for_load_state(self, state: str = "domcontentloaded") -> None:
        """Wait for page load state."""
        self.page.wait_for_load_state(state)
        
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """Wait for element to be visible."""
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for element: {selector}")
        return self.page.wait_for_selector(selector, timeout=timeout)
        
    def click_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click on an element."""
        timeout = timeout or self.timeout
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout)
        
    def fill_input(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Fill input field with text."""
        timeout = timeout or self.timeout
        logger.info(f"Filling input {selector} with: {text}")
        self.page.fill(selector, text, timeout=timeout)
        
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get text content of an element."""
        timeout = timeout or self.timeout
        return self.page.text_content(selector, timeout=timeout) or ""
        
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False
            
    def is_hidden(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is hidden."""
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            return True
        except Exception:
            return False
            
    def take_screenshot(self, name: Optional[str] = None) -> str:
        """Take a screenshot of the current page."""
        if not name:
            name = f"screenshot_{self.__class__.__name__}.png"
        
        screenshot_path = f"reports/screenshots/{name}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
        
    def scroll_to_element(self, selector: str) -> None:
        """Scroll to make element visible."""
        logger.info(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
        
    def wait_for_url_contains(self, url_part: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to contain specific text."""
        timeout = timeout or self.timeout
        self.page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
        
    def press_key(self, key: str) -> None:
        """Press a keyboard key."""
        logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)
        
    def hover_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """Hover over an element."""
        timeout = timeout or self.timeout
        logger.info(f"Hovering over element: {selector}")
        self.page.hover(selector, timeout=timeout) 