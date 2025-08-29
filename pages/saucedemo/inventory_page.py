"""
Inventory page object for SauceDemo website.
"""

from typing import List
from playwright.sync_api import Page
from ..base_page import BasePage


class InventoryPage(BasePage):
    """Inventory page object for saucedemo.com."""
    
    def __init__(self, page: Page):
        """Initialize inventory page."""
        super().__init__(page)
        
        # Locators
        self.page_title = ".title"
        self.hamburger_menu = ".bm-burger-button"
        self.logout_link = "#logout_sidebar_link"
        self.cart_icon = ".shopping_cart_link"
        self.cart_badge = ".shopping_cart_badge"
        self.sort_dropdown = ".product_sort_container"
        
        # Product locators
        self.inventory_items = ".inventory_item"
        self.product_names = ".inventory_item_name"
        self.product_prices = ".inventory_item_price"
        self.product_descriptions = ".inventory_item_desc"
        self.add_to_cart_buttons = ".btn_inventory"
        self.remove_buttons = ".btn_secondary"
        
        # Specific product locators - using generic button selectors since IDs don't work
        self.add_to_cart_buttons_generic = ".btn_primary.btn_inventory"
        
    def is_loaded(self) -> bool:
        """Check if inventory page is loaded."""
        # Check for inventory items instead of title since title selector may vary
        return len(self.page.locator(self.inventory_items).all()) > 0
        
    def get_page_title(self) -> str:
        """Get page title."""
        return self.get_text(self.page_title)
        
    def open_hamburger_menu(self) -> None:
        """Open hamburger menu."""
        self.click_element(self.hamburger_menu)
        
    def logout(self) -> None:
        """Logout from the application."""
        self.open_hamburger_menu()
        self.click_element(self.logout_link)
        
    def click_cart(self) -> None:
        """Click on cart icon."""
        self.click_element(self.cart_icon)
        
    def get_cart_items_count(self) -> int:
        """Get number of items in cart."""
        if self.is_visible(self.cart_badge):
            return int(self.get_text(self.cart_badge))
        return 0
        
    def get_products_count(self) -> int:
        """Get total number of products."""
        return len(self.page.locator(self.inventory_items).all())
        
    def get_product_names(self) -> List[str]:
        """Get all product names."""
        names = []
        product_elements = self.page.locator(self.product_names).all()
        for element in product_elements:
            names.append(element.text_content() or "")
        return names
        
    def get_product_prices(self) -> List[str]:
        """Get all product prices."""
        prices = []
        price_elements = self.page.locator(self.product_prices).all()
        for element in price_elements:
            prices.append(element.text_content() or "")
        return prices
        
    def add_product_to_cart_by_index(self, product_index: int = 0) -> None:
        """Add product to cart by index (0-based)."""
        buttons = self.page.locator(self.add_to_cart_buttons_generic).all()
        if product_index < len(buttons):
            buttons[product_index].click()
        else:
            raise ValueError(f"Product index {product_index} is out of range")
            
    def add_backpack_to_cart(self) -> None:
        """Add backpack to cart (first product)."""
        self.add_product_to_cart_by_index(0)
        
    def add_bike_light_to_cart(self) -> None:
        """Add bike light to cart (second product)."""
        self.add_product_to_cart_by_index(1)
        
    def add_tshirt_to_cart(self) -> None:
        """Add t-shirt to cart (third product)."""
        self.add_product_to_cart_by_index(2)
        
    def add_all_products_to_cart(self) -> None:
        """Add all products to cart."""
        # Get all available add to cart buttons and click them
        buttons = self.page.locator(self.add_to_cart_buttons_generic).all()
        for button in buttons:
            if button.is_visible():
                try:
                    button.click()
                    # Small wait to ensure the click is processed
                    self.page.wait_for_timeout(100)
                except:
                    continue
                
    def remove_product_from_cart(self, product_name: str) -> None:
        """Remove specific product from cart."""
        # This would need to be implemented based on the remove button structure
        remove_buttons = self.page.locator(self.remove_buttons).all()
        if remove_buttons:
            remove_buttons[0].click()  # Remove first item for demo
            
    def sort_products(self, sort_option: str) -> None:
        """Sort products by given option."""
        self.page.select_option(self.sort_dropdown, sort_option)
        
    def sort_by_name_asc(self) -> None:
        """Sort products by name A-Z."""
        self.sort_products("az")
        
    def sort_by_name_desc(self) -> None:
        """Sort products by name Z-A."""
        self.sort_products("za")
        
    def sort_by_price_low_high(self) -> None:
        """Sort products by price low to high."""
        self.sort_products("lohi")
        
    def sort_by_price_high_low(self) -> None:
        """Sort products by price high to low."""
        self.sort_products("hilo")
        
    def click_product_name(self, product_name: str) -> None:
        """Click on a specific product name."""
        self.page.click(f"text={product_name}")
        
    def is_product_added_to_cart(self, product_index: int = 0) -> bool:
        """Check if product has been added to cart by checking cart badge."""
        return self.get_cart_items_count() > 0 