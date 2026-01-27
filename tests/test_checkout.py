"""
Test suite for SauceDemo checkout functionality.
Covers complete checkout flow, form validation, and order confirmation.
"""
import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import BASE_URL
from utils.helpers import load_test_data

BASE_URL_NO_SLASH = BASE_URL.rstrip("/")


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
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        # Fill checkout information
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        checkout_page.continue_to_overview()
        
        # Verify overview page
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-two.html")
        assert checkout_page.is_overview_loaded(), "Checkout overview should be loaded"
        
        # Complete order
        checkout_page.finish_order()
        
        # Verify order completion
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-complete.html")
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
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        # Fill form with missing first name
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"
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
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-one.html")
    
    def test_checkout_missing_last_name(self, inventory_page: InventoryPage):
        """Test checkout form validation - missing last name."""
        test_data = load_test_data()
        
        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["bike_light"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        # Fill form with missing last name
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"
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
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        # Fill form with missing postal code
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"
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
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        # Cancel checkout
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before cancel"
        checkout_page.cancel_checkout()
        
        # Verify return to cart
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/cart.html")
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
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/")
    
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
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"
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

    def test_back_and_forward_in_checkout_flow(self, inventory_page: InventoryPage):
        """Using browser back/forward should keep checkout flow consistent."""
        test_data = load_test_data()

        # Add item and proceed to checkout step one
        item_name = test_data["products"]["backpack"]
        inventory_page.add_item_to_cart(item_name)
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        assert cart_page.is_loaded(), "Cart page should be loaded before proceeding to checkout"
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(inventory_page.page)
        assert checkout_page.is_step_one_loaded(), "Checkout step one should be loaded before filling data"

        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"],
        )
        checkout_page.continue_to_overview()

        # We should be on step two (overview)
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-two.html")
        assert checkout_page.is_overview_loaded(), "Checkout overview should be loaded"

        # Use browser back to return to step one, values should still be present
        page = inventory_page.page
        page.go_back()
        expect(page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-one.html")
        # Swag Labs clears the form inputs when navigating back from step two.
        assert checkout_page.first_name_input.input_value() == ""
        assert checkout_page.last_name_input.input_value() == ""
        assert checkout_page.postal_code_input.input_value() == ""

        # Use browser forward to go back to step two
        page.go_forward()
        expect(page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-two.html")
        assert checkout_page.is_overview_loaded(), "Checkout overview should be loaded after going forward"

    def test_overview_items_match_cart_items(self, inventory_page: InventoryPage):
        """Items shown on checkout overview should match items in the cart."""
        test_data = load_test_data()

        items = [
            test_data["products"]["backpack"],
            test_data["products"]["bike_light"],
        ]

        # Add items and go to cart
        for item in items:
            inventory_page.add_item_to_cart(item)
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_items = cart_page.get_items()
        cart_names = sorted([item["name"] for item in cart_items])

        # Proceed to checkout overview
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"],
        )
        checkout_page.continue_to_overview()

        overview_items = checkout_page.get_overview_items()
        overview_names = sorted([item["name"] for item in overview_items])

        assert cart_names == overview_names, "Overview items should match cart items"

    def test_totals_and_tax_calculation_on_overview(self, inventory_page: InventoryPage):
        """Total on overview page should equal subtotal + tax."""
        test_data = load_test_data()

        # Add a few items
        items = [
            test_data["products"]["backpack"],
            test_data["products"]["bike_light"],
            test_data["products"]["bolt_tshirt"],
        ]
        for item in items:
            inventory_page.add_item_to_cart(item)

        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(inventory_page.page)
        customer_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"],
        )
        checkout_page.continue_to_overview()

        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()

        assert subtotal > 0, "Subtotal should be greater than zero"
        assert tax >= 0, "Tax should be non-negative"
        # Allow for small floating point differences
        expected_total = subtotal + tax
        assert abs(total - expected_total) < 0.01, (
            f"Total {total} should equal subtotal + tax {expected_total}"
        )

    def test_error_message_clears_after_correcting_checkout_info(
        self, inventory_page: InventoryPage
    ):
        """
        When checkout info is corrected after an error, the user
        should be able to proceed to the overview page.
        """
        test_data = load_test_data()

        # Add item and proceed to checkout
        inventory_page.add_item_to_cart(test_data["products"]["backpack"])
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(inventory_page.page)

        # First, trigger an error by omitting first name
        invalid_info = test_data["checkout"]["missing_first_name"]
        checkout_page.fill_customer_info(
            invalid_info["first_name"],
            invalid_info["last_name"],
            invalid_info["postal_code"],
        )
        checkout_page.continue_to_overview()
        error_message = checkout_page.get_error_message()
        assert "First Name is required" in error_message or "Error" in error_message

        # Now correct the information
        valid_info = test_data["checkout"]["valid"]
        checkout_page.fill_customer_info(
            valid_info["first_name"],
            valid_info["last_name"],
            valid_info["postal_code"],
        )
        checkout_page.continue_to_overview()

        # Error should be cleared and we should be on step two
        assert checkout_page.get_error_message() == ""
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-two.html")
