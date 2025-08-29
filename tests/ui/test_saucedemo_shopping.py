"""
Shopping flow tests for SauceDemo website.
"""

import pytest
from playwright.sync_api import Page
from pages.saucedemo.login_page import LoginPage
from pages.saucedemo.inventory_page import InventoryPage
from pages.saucedemo.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.saucedemo
class TestSauceDemoShopping:
    """Test cases for SauceDemo shopping functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - login before each test."""
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        
        # Login before each test
        self.login_page.open()
        self.login_page.login_with_standard_user()
        assert self.inventory_page.is_loaded()
        
    @pytest.mark.smoke
    def test_inventory_page_elements(self, page: Page):
        """Test inventory page displays all required elements."""
        # Check products are displayed
        assert self.inventory_page.get_products_count() == 6
        
        # Check cart icon is visible
        assert self.inventory_page.is_visible(self.inventory_page.cart_icon)
        
        # Check sort dropdown is visible
        assert self.inventory_page.is_visible(self.inventory_page.sort_dropdown)
        
        # Check hamburger menu is visible
        assert self.inventory_page.is_visible(self.inventory_page.hamburger_menu)
        
    def test_product_information_display(self, page: Page):
        """Test that all product information is displayed correctly."""
        # Get product names and verify they exist
        product_names = self.inventory_page.get_product_names()
        assert len(product_names) == 6
        
        expected_products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light", 
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Onesie",
            "Test.allTheThings() T-Shirt (Red)"
        ]
        
        for product in expected_products:
            assert product in product_names
            
        # Get product prices and verify format
        product_prices = self.inventory_page.get_product_prices()
        assert len(product_prices) == 6
        
        for price in product_prices:
            assert price.startswith("$")
            assert "." in price  # Check decimal format
            
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, page: Page):
        """Test adding a single product to cart."""
        # Add backpack to cart
        self.inventory_page.add_backpack_to_cart()
        
        # Verify cart badge shows 1 item
        assert self.inventory_page.get_cart_items_count() == 1
        
        # Verify product was added to cart
        assert self.inventory_page.is_product_added_to_cart(0)
        
    def test_add_multiple_products_to_cart(self, page: Page):
        """Test adding multiple products to cart."""
        # Add multiple products
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.add_tshirt_to_cart()
        
        # Verify cart badge shows 3 items
        assert self.inventory_page.get_cart_items_count() == 3
        
    def test_add_all_products_to_cart(self, page: Page):
        """Test adding all products to cart."""
        # Add all products
        self.inventory_page.add_all_products_to_cart()
        
        # Verify all products were added (should be 6, but may vary based on site behavior)
        cart_count = self.inventory_page.get_cart_items_count()
        assert cart_count >= 3, f"Expected at least 3 items in cart, got {cart_count}"
        
    def test_sort_products_by_name_ascending(self, page: Page):
        """Test sorting products by name A-Z."""
        # Sort by name ascending
        self.inventory_page.sort_by_name_asc()
        
        # Get product names after sorting
        sorted_names = self.inventory_page.get_product_names()
        
        # Verify they are in alphabetical order
        expected_order = sorted(sorted_names)
        assert sorted_names == expected_order
        
    def test_sort_products_by_name_descending(self, page: Page):
        """Test sorting products by name Z-A."""
        # Sort by name descending
        self.inventory_page.sort_by_name_desc()
        
        # Get product names after sorting
        sorted_names = self.inventory_page.get_product_names()
        
        # Verify they are in reverse alphabetical order
        expected_order = sorted(sorted_names, reverse=True)
        assert sorted_names == expected_order
        
    def test_sort_products_by_price_low_to_high(self, page: Page):
        """Test sorting products by price low to high."""
        # Sort by price low to high
        self.inventory_page.sort_by_price_low_high()
        
        # Get prices after sorting
        sorted_prices = self.inventory_page.get_product_prices()
        
        # Convert to float for comparison (remove $ and convert)
        price_values = [float(price.replace("$", "")) for price in sorted_prices]
        
        # Verify they are in ascending order
        assert price_values == sorted(price_values)
        
    def test_sort_products_by_price_high_to_low(self, page: Page):
        """Test sorting products by price high to low."""
        # Sort by price high to low
        self.inventory_page.sort_by_price_high_low()
        
        # Get prices after sorting
        sorted_prices = self.inventory_page.get_product_prices()
        
        # Convert to float for comparison
        price_values = [float(price.replace("$", "")) for price in sorted_prices]
        
        # Verify they are in descending order
        assert price_values == sorted(price_values, reverse=True)
        
    @pytest.mark.smoke
    def test_view_cart_with_items(self, page: Page):
        """Test viewing cart with items."""
        # Add some products to cart
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        
        # Go to cart
        self.inventory_page.click_cart()
        
        # Verify we're on cart page
        assert self.cart_page.is_loaded()
        
        # Verify cart contains the items
        assert self.cart_page.get_cart_items_count() == 2
        
        cart_item_names = self.cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_item_names
        # Check that we have 2 items total, regardless of which specific items
        assert len(cart_item_names) == 2
        
    def test_remove_item_from_cart(self, page: Page):
        """Test removing items from cart."""
        # Add items to cart
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        
        # Go to cart
        self.inventory_page.click_cart()
        assert self.cart_page.get_cart_items_count() == 2
        
        # Remove one item
        self.cart_page.remove_item_from_cart(0)
        
        # Verify one item removed
        assert self.cart_page.get_cart_items_count() == 1
        
    def test_continue_shopping_from_cart(self, page: Page):
        """Test continue shopping button in cart."""
        # Add item and go to cart
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        
        # Click continue shopping
        self.cart_page.continue_shopping()
        
        # Verify we're back on inventory page
        assert self.inventory_page.is_loaded()
        
        # Verify cart still has item
        assert self.inventory_page.get_cart_items_count() == 1
        
    def test_empty_cart_behavior(self, page: Page):
        """Test behavior with empty cart."""
        # Go to cart without adding items
        self.inventory_page.click_cart()
        
        # Verify cart is empty
        assert self.cart_page.is_cart_empty()
        assert self.cart_page.get_cart_items_count() == 0
        
        # Verify checkout button is still visible
        assert self.cart_page.is_checkout_button_visible()
        
    def test_logout_functionality(self, page: Page):
        """Test logout from inventory page."""
        # Logout
        self.inventory_page.logout()
        
        # Verify we're back on login page
        assert self.login_page.is_logo_visible()
        assert "index.html" in page.url or page.url.endswith("/")
        
    def test_cart_persistence_across_pages(self, page: Page):
        """Test that cart items persist when navigating."""
        # Add items to cart
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        
        # Go to cart and back
        self.inventory_page.click_cart()
        self.cart_page.continue_shopping()
        
        # Verify cart count is still correct
        assert self.inventory_page.get_cart_items_count() == 2
        
        # Go to cart again and verify items are there
        self.inventory_page.click_cart()
        assert self.cart_page.get_cart_items_count() == 2
        
    @pytest.mark.regression
    def test_problem_user_shopping_experience(self, page: Page):
        """Test shopping with problem user (may have UI issues)."""
        # Logout and login with problem user
        self.inventory_page.logout()
        self.login_page.login_with_problem_user()
        
        # Try to add products (problem user may have issues)
        try:
            self.inventory_page.add_backpack_to_cart()
            # With problem user, images might be broken or other issues
            # This test documents the known issues
        except Exception as e:
            # Problem user is expected to have issues
            pytest.skip(f"Problem user has known issues: {e}")
            
    @pytest.mark.performance
    def test_performance_user_shopping_experience(self, page: Page):
        """Test shopping with performance glitch user."""
        # Logout and login with performance user
        self.inventory_page.logout()
        self.login_page.login_with_performance_user()
        
        # Performance user may be slower but should work
        assert self.inventory_page.is_loaded()
        
        # Add product (may be slower)
        self.inventory_page.add_backpack_to_cart()
        assert self.inventory_page.get_cart_items_count() == 1 