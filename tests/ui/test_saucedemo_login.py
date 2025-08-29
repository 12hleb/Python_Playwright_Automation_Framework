"""
Login tests for SauceDemo website.
"""

import pytest
from playwright.sync_api import Page
from pages.saucedemo.login_page import LoginPage
from pages.saucedemo.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.saucedemo
class TestSauceDemoLogin:
    """Test cases for SauceDemo login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test."""
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.login_page.open()
        
    @pytest.mark.smoke
    def test_successful_login_standard_user(self, page: Page):
        """Test successful login with standard user."""
        # Login with standard user
        self.login_page.login_with_standard_user()
        
        # Verify successful login
        assert self.inventory_page.is_loaded()
        assert "inventory.html" in page.url
        
    @pytest.mark.smoke
    def test_successful_login_problem_user(self, page: Page):
        """Test successful login with problem user."""
        # Login with problem user
        self.login_page.login_with_problem_user()
        
        # Verify successful login
        assert self.inventory_page.is_loaded()
        
    def test_successful_login_performance_user(self, page: Page):
        """Test successful login with performance glitch user."""
        # Login with performance user
        self.login_page.login_with_performance_user()
        
        # Verify successful login (may take longer)
        assert self.inventory_page.is_loaded()
        
    def test_locked_out_user_login(self, page: Page):
        """Test login with locked out user shows error."""
        # Try to login with locked out user
        self.login_page.login_with_locked_user()
        
        # Verify error message is displayed
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "locked out" in error_text.lower()
        
        # Verify still on login page
        assert self.login_page.is_logo_visible()
        
    def test_invalid_username_login(self, page: Page):
        """Test login with invalid username."""
        # Try login with invalid credentials
        self.login_page.login("invalid_user", "secret_sauce")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Username and password do not match" in error_text
        
    def test_invalid_password_login(self, page: Page):
        """Test login with invalid password."""
        # Try login with invalid password
        self.login_page.login("standard_user", "wrong_password")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Username and password do not match" in error_text
        
    def test_empty_username_login(self, page: Page):
        """Test login with empty username."""
        # Try login with empty username
        self.login_page.login("", "secret_sauce")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Username is required" in error_text
        
    def test_empty_password_login(self, page: Page):
        """Test login with empty password."""
        # Try login with empty password
        self.login_page.login("standard_user", "")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Password is required" in error_text
        
    def test_empty_credentials_login(self, page: Page):
        """Test login with both fields empty."""
        # Try login with empty credentials
        self.login_page.login("", "")
        
        # Verify error message
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Username is required" in error_text
        
    def test_error_message_close(self, page: Page):
        """Test closing error message."""
        # Generate an error
        self.login_page.login("", "")
        assert self.login_page.is_error_displayed()
        
        # Close error message
        self.login_page.close_error_message()
        
        # Verify error is hidden
        assert not self.login_page.is_error_displayed()
        
    def test_login_form_validation(self, page: Page):
        """Test login form field validation."""
        # Verify login button is enabled by default
        assert self.login_page.is_login_button_enabled()
        
        # Test field clearing
        self.login_page.fill_input(self.login_page.username_input, "test")
        self.login_page.fill_input(self.login_page.password_input, "test")
        
        # Clear fields
        self.login_page.clear_username()
        self.login_page.clear_password()
        
        # Verify fields are empty
        assert self.login_page.get_username_value() == ""
        assert self.login_page.get_password_value() == ""
        
    def test_case_sensitive_credentials(self, page: Page):
        """Test that credentials are case sensitive."""
        # Try with uppercase username
        self.login_page.login("STANDARD_USER", "secret_sauce")
        
        # Should show error
        assert self.login_page.is_error_displayed()
        
        # Try with wrong case password
        self.login_page.clear_username()
        self.login_page.clear_password()
        self.login_page.login("standard_user", "SECRET_SAUCE")
        
        # Should show error
        assert self.login_page.is_error_displayed()
        
    @pytest.mark.regression
    def test_sql_injection_protection(self, page: Page):
        """Test protection against SQL injection attempts."""
        # Try basic SQL injection
        self.login_page.login("admin' OR '1'='1", "password")
        
        # Should show normal error, not break
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert "Username and password do not match" in error_text
        
    @pytest.mark.regression
    def test_xss_protection(self, page: Page):
        """Test protection against XSS attacks."""
        # Try basic XSS
        self.login_page.login("<script>alert('xss')</script>", "password")
        
        # Should show normal error, not execute script
        assert self.login_page.is_error_displayed()
        
    def test_login_page_elements(self, page: Page):
        """Test all login page elements are present."""
        # Check all required elements are visible
        assert self.login_page.is_logo_visible()
        assert self.login_page.is_visible(self.login_page.username_input)
        assert self.login_page.is_visible(self.login_page.password_input)
        assert self.login_page.is_visible(self.login_page.login_button)
        
        # Check placeholder text or labels if needed
        username_placeholder = page.get_attribute(self.login_page.username_input, "placeholder")
        password_placeholder = page.get_attribute(self.login_page.password_input, "placeholder")
        
        assert username_placeholder == "Username"
        assert password_placeholder == "Password" 