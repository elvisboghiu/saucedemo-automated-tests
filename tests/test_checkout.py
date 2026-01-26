"""
Test suite for SauceDemo checkout functionality.
Covers complete checkout flow, form validation, and order confirmation.
"""
import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import load_test_data


@pytest.mark.checkout
class TestCheckout:
    """Test cases for checkout functionality."""
    
    def test_complete_checkout_flow(self, inventory_page: InventoryPage):
        """Test complete end-to-end checkout process."""
        test_data = load_test_data()
        
        # Add items to cart
        item1 = test_data["products"]["backpack"]
        item2 = test_data["products"]["bike_light"]
        inventory_page.add_item_to_cart(item1)
        inventory_page.add_item_to_cart(item2)
        
        # Navigate to cart and proceed to checkout
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        # Fill checkout information
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        
        # Verify overview page
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
        
        # Complete order
        checkout_page.finish_order()
        
        # Verify order completion
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
        assert checkout_page.is_checkout_complete(), "Checkout should be complete"
        
        confirmation_message = checkout_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation_message, \
            f"Expected confirmation message. Got: {confirmation_message}"
        
        # Verify cart is cleared (by checking we can navigate back)
        checkout_page.back_to_home()
        inventory_page = InventoryPage(inventory_page.page)
        assert inventory_page.get_cart_count() == 0, "Cart should be empty after order completion"
    
    def test_checkout_missing_first_name(self, inventory_page: InventoryPage):
        """Test checkout form validation - missing first name."""
        test_data = load_test_data()
        
        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["backpack"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        # Fill form with missing first name
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["missing_first_name"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        
        # Verify error message
        error_message = checkout_page.get_error_message()
        assert "First Name is required" in error_message or \
               "Error" in error_message, \
               f"Expected error for missing first name. Got: {error_message}"
        
        # Verify still on checkout page
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
    
    def test_checkout_missing_last_name(self, inventory_page: InventoryPage):
        """Test checkout form validation - missing last name."""
        test_data = load_test_data()
        
        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["bike_light"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        # Fill form with missing last name
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["missing_last_name"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        
        # Verify error message
        error_message = checkout_page.get_error_message()
        assert "Last Name is required" in error_message or \
               "Error" in error_message, \
               f"Expected error for missing last name. Got: {error_message}"
    
    def test_checkout_missing_postal_code(self, inventory_page: InventoryPage):
        """Test checkout form validation - missing postal code."""
        test_data = load_test_data()
        
        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["bolt_tshirt"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        # Fill form with missing postal code
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["missing_postal_code"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        
        # Verify error message
        error_message = checkout_page.get_error_message()
        assert "Postal Code is required" in error_message or \
               "Error" in error_message, \
               f"Expected error for missing postal code. Got: {error_message}"
    
    def test_cancel_checkout(self, inventory_page: InventoryPage):
        """Test canceling checkout returns to cart."""
        test_data = load_test_data()
        
        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["fleece_jacket"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        # Cancel checkout
        checkout_page = CheckoutPage(inventory_page.page)
        checkout_page.cancel_checkout()
        
        # Verify return to cart
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/cart.html")
        cart_page = CartPage(inventory_page.page)
        assert cart_page.is_loaded(), "Should be back on cart page"
    
    def test_logout_from_inventory_after_checkout(self, inventory_page: InventoryPage):
        """Test logout functionality from inventory page."""
        test_data = load_test_data()
        
        # Complete a checkout flow first
        inventory_page.add_item_to_cart(test_data["products"]["onesie"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_order()
        checkout_page.back_to_home()
        
        # Logout
        inventory_page = InventoryPage(inventory_page.page)
        inventory_page.logout()
        
        # Verify redirect to login page
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/")
    
    def test_checkout_with_multiple_items(self, inventory_page: InventoryPage):
        """Test checkout process with multiple items in cart."""
        test_data = load_test_data()
        
        # Add multiple items
        items = [
            test_data["products"]["backpack"],
            test_data["products"]["bike_light"],
            test_data["products"]["bolt_tshirt"]
        ]
        for item in items:
            inventory_page.add_item_to_cart(item)
        
        assert inventory_page.get_cart_count() == len(items), "All items should be in cart"
        
        # Proceed through checkout
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        checkout_page.finish_order()
        
        # Verify completion
        assert checkout_page.is_checkout_complete(), "Checkout should complete successfully"
