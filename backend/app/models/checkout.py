from flask import session
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product


class Checkout:
    @staticmethod
    def process_checkout(user_id):
        """Process checkout, create an order, and deduct stock"""
        cart = session.get("cart", [])
        if not cart:
            return {"error": "Cart is empty"}, 400

        total_price = 0
        order_items = []

        for item in cart:
            product = Product.query.get(item["product_id"])
            if not product:
                return {"error": f"Product ID {item['product_id']} not found"}, 404

            if product.stock < item["quantity"]:
                return {"error": f"Not enough stock for {product.name}"}, 400

            product.stock -= item["quantity"]  # Deduct stock
            total_price += product.price * item["quantity"]
            order_items.append(
                OrderItem(product_id=product.id, quantity=item["quantity"], price_at_purchase=product.price))

        # Create the order
        new_order = Order(user_id=user_id, total_price=total_price)
        db.session.add(new_order)
        db.session.flush()  # Get order ID

        # Link order items to the order
        for item in order_items:
            item.order_id = new_order.id
            db.session.add(item)

        db.session.commit()

        # Clear cart after successful checkout
        session["cart"] = []
        session.modified = True

        return {"message": "Order placed successfully", "order_id": new_order.id}, 201
