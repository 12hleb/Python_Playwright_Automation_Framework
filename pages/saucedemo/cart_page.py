"""
Cart page object for SauceDemo website.
"""

from typing import List
from playwright.sync_api import Page
from ..base_page import BasePage


class CartPage(BasePage):
    """Cart page object for saucedemo.com."""
    
    def __init__(self, page: Page):
        """Initialize cart page."""
        super().__init__(page)
        
        # Locators
        self.page_title = ".title"
        self.continue_shopping_button = "a.btn_secondary"
        self.checkout_button = "a.btn_action.checkout_button"
        self.cart_items = ".cart_item"
        self.cart_item_names = ".inventory_item_name"
        self.cart_item_prices = ".inventory_item_price"
        self.cart_item_descriptions = ".inventory_item_desc"
        self.remove_buttons = ".btn_secondary"
        self.cart_quantity = ".cart_quantity"
        
        # Hamburger menu
        self.hamburger_menu = ".bm-burger-button"
        self.logout_link = "#logout_sidebar_link"
        
    def is_loaded(self) -> bool:
        """Check if cart page is loaded."""
        try:
            # Wait for page to load and check URL
            self.page.wait_for_load_state("networkidle", timeout=10000)
            return "cart.html" in self.page.url
        except:
            return "cart.html" in self.page.url
        
    def get_page_title(self) -> str:
        """Get page title."""
        return self.get_text(self.page_title)
        
    def continue_shopping(self) -> None:
        """Click continue shopping button."""
        self.click_element(self.continue_shopping_button)
        
    def proceed_to_checkout(self) -> None:
        """Click checkout button."""
        self.click_element(self.checkout_button)
        
    def get_cart_items_count(self) -> int:
        """Get number of items in cart."""
        return len(self.page.locator(self.cart_items).all())
        
    def get_cart_item_names(self) -> List[str]:
        """Get names of all items in cart."""
        names = []
        name_elements = self.page.locator(self.cart_item_names).all()
        for element in name_elements:
            names.append(element.text_content() or "")
        return names
        
    def get_cart_item_prices(self) -> List[str]:
        """Get prices of all items in cart."""
        prices = []
        price_elements = self.page.locator(self.cart_item_prices).all()
        for element in price_elements:
            prices.append(element.text_content() or "")
        return prices
        
    def remove_item_from_cart(self, item_index: int = 0) -> None:
        """Remove item from cart by index."""
        remove_buttons = self.page.locator(self.remove_buttons).all()
        if item_index < len(remove_buttons):
            remove_buttons[item_index].click()
            
    def remove_all_items(self) -> None:
        """Remove all items from cart."""
        while self.get_cart_items_count() > 0:
            self.remove_item_from_cart(0)
            
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.get_cart_items_count() == 0
        
    def is_checkout_button_visible(self) -> bool:
        """Check if checkout button is visible."""
        return self.is_visible(self.checkout_button)
        
    def is_continue_shopping_button_visible(self) -> bool:
        """Check if continue shopping button is visible."""
        return self.is_visible(self.continue_shopping_button)
        
    def logout(self) -> None:
        """Logout from the application."""
        self.click_element(self.hamburger_menu)
        self.click_element(self.logout_link) 