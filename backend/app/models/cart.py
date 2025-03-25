from flask import session


class Cart:
    @staticmethod
    def add_to_cart(product_id, quantity):
        """Add products to the cart session"""
        if "cart" not in session:
            session["cart"] = []

        # Check if the product already exists in the cart
        for item in session["cart"]:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            session["cart"].append({"product_id": product_id, "quantity": quantity})

        session.modified = True  # Ensure session updates
        return session["cart"]

    @staticmethod
    def remove_from_cart(product_id):
        """Remove a product from the cart"""
        if "cart" in session:
            session["cart"] = [item for item in session["cart"] if item["product_id"] != product_id]
            session.modified = True
        return session["cart"]

    @staticmethod
    def clear_cart():
        """Clear all items from the cart"""
        session["cart"] = []
        session.modified = True
        return session["cart"]

    @staticmethod
    def get_cart():
        """Retrieve current cart items"""
        return session.get("cart", [])
