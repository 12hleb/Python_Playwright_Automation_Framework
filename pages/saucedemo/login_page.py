"""
Login page object for SauceDemo website.
"""

from playwright.sync_api import Page
from ..base_page import BasePage


class LoginPage(BasePage):
    """Login page object for saucedemo.com."""
    
    def __init__(self, page: Page):
        """Initialize login page."""
        super().__init__(page)
        
        # Locators
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "[data-test='error']"
        self.error_close_button = ".error-button"
        self.logo = ".login_logo"
        
        # Test credentials from the website
        self.valid_users = {
            'standard_user': 'secret_sauce',
            'problem_user': 'secret_sauce',
            'performance_glitch_user': 'secret_sauce'
        }
        self.locked_user = 'locked_out_user'
        self.password = 'secret_sauce'
        
    def open(self) -> None:
        """Open the login page."""
        self.navigate_to("https://www.saucedemo.com/v1/")
        self.wait_for_load_state()
        
    def login(self, username: str, password: str) -> None:
        """Login with provided credentials."""
        self.fill_input(self.username_input, username)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)
        # Wait for navigation to complete
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
    def login_with_standard_user(self) -> None:
        """Login with standard user credentials."""
        self.login('standard_user', 'secret_sauce')
        
    def login_with_problem_user(self) -> None:
        """Login with problem user credentials."""
        self.login('problem_user', 'secret_sauce')
        
    def login_with_performance_user(self) -> None:
        """Login with performance glitch user credentials."""
        self.login('performance_glitch_user', 'secret_sauce')
        
    def login_with_locked_user(self) -> None:
        """Login with locked out user credentials."""
        self.login('locked_out_user', 'secret_sauce')
        
    def get_error_message(self) -> str:
        """Get the error message text."""
        return self.get_text(self.error_message)
        
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_visible(self.error_message)
        
    def close_error_message(self) -> None:
        """Close the error message."""
        if self.is_visible(self.error_close_button):
            self.click_element(self.error_close_button)
            
    def is_logo_visible(self) -> bool:
        """Check if logo is visible."""
        return self.is_visible(self.logo)
        
    def clear_username(self) -> None:
        """Clear username field."""
        self.page.fill(self.username_input, "")
        
    def clear_password(self) -> None:
        """Clear password field."""
        self.page.fill(self.password_input, "")
        
    def get_username_value(self) -> str:
        """Get current username field value."""
        return self.page.input_value(self.username_input)
        
    def get_password_value(self) -> str:
        """Get current password field value."""
        return self.page.input_value(self.password_input)
        
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        return self.page.is_enabled(self.login_button) 