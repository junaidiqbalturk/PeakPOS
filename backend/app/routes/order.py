from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.activity_log import log_activity  # Import log function

order_bp = Blueprint("order", __name__)


#  Create New Order
@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get user ID from JWT token

    if not data or "items" not in data:
        return jsonify({"error": "Invalid request, missing items"}), 400

    total_price = 0
    order_items = []

    for item in data["items"]:
        product = Product.query.get(item["product_id"])
        if not product:
            return jsonify({"error": f"Product ID {item['product_id']} not found"}), 404

        if product.stock < item["quantity"]:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400

        product.stock -= item["quantity"]  # ✅ Reduce stock after purchase
        total_price += product.price * item["quantity"]
        order_items.append(OrderItem(product_id=product.id, quantity=item["quantity"], price_at_purchase=product.price))

    # Create Order
    new_order = Order(user_id=user_id, total_price=total_price)
    db.session.add(new_order)
    db.session.flush()  # Get order ID before commit

    for item in order_items:
        item.order_id = new_order.id  # Assign order ID
        db.session.add(item)

    db.session.commit()
    # Log the order creation
    log_entry=log_activity(user_id, "Created Order", f"Order ID {new_order.id}, Total: ${total_price}")
    db.session.add(log_entry)
    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201


# Get All Orders for specific User
@order_bp.route("/orders", methods=["GET"])
@jwt_required()  # Ensure user is authenticated
def get_orders():
    """Fetch all orders for the logged-in user."""
    user_id = get_jwt_identity()  # Get user ID from JWT

    orders = Order.query.filter_by(user_id=user_id).all()

    order_list = []
    for order in orders:
        order_data = {
            "order_id": order.id,
            "total_price": order.total_price,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": []
        }

        for item in order.order_items:
            order_data["items"].append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price_at_purchase
            })

        order_list.append(order_data)

    return jsonify(order_list), 200


# Get Order by ID
@order_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order_by_id(order_id):
    """Fetch details of a specific order"""
    user_id = get_jwt_identity()  # Get user ID from JWT

    # Fetch the order, ensuring it belongs to the logged-in user
    order = Order.query.options(db.joinedload(Order.order_items)).filter_by(id=order_id, user_id=user_id).first()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Build response
    order_data = {
        "order_id": order.id,
        "total_price": order.total_price,
        "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "items": []
    }

    for item in order.order_items:
        order_data["items"].append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price_at_purchase
        })

    return jsonify(order_data), 200


# Delete Order
@order_bp.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    """Cancel an order (only if it belongs to the user)"""
    user_id = get_jwt_identity()  # Get user ID from JWT

    # Fetch the order, ensuring it belongs to the logged-in user
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()

    if not order:
        return jsonify({"error": "Order not found or unauthorized"}), 404

    # Delete the order and associated items
    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully"}), 200


@order_bp.route("/orders/<int:order_id>", methods=["PUT"])
@jwt_required()
def update_order(order_id):
    """Update an existing order (only if it belongs to the user)"""
    user_id = get_jwt_identity()  # Get user ID from JWT
    data = request.get_json()

    # Fetch the order, ensuring it belongs to the logged-in user
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()

    if not order:
        return jsonify({"error": "Order not found or unauthorized"}), 404

    # Initialize new total price
    new_total_price = 0

    # Update order items if provided
    if "items" in data:
        for item_data in data["items"]:
            item = next((i for i in order.order_items if i.product_id == item_data["product_id"]), None)

            if item:
                # Fetch the product price from the Product table
                product = Product.query.get(item.product_id)
                if not product:
                    return jsonify({"error": f"Product ID {item_data['product_id']} not found"}), 400

                # Update the quantity and recalculate the price correctly
                item.quantity = item_data["quantity"]
                item.price_at_purchase = item.quantity * product.price  # Corrected calculation
                new_total_price += item.price_at_purchase
            else:
                return jsonify({"error": f"Product ID {item_data['product_id']} not found in order"}), 400

    # Update order total price
    order.total_price = new_total_price

    db.session.commit()

    return jsonify({"message": "Order updated successfully"}), 200


# Get Admin View for All Orders
@order_bp.route("/admin/orders", methods=["GET"])
@jwt_required()
def get_all_orders():
    """Fetch all orders (Admin-only)"""
    user_id = get_jwt_identity()  # Get user ID from JWT

    # Fetch user role
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized, admin access only"}), 403

    # Fetch all orders
    orders = Order.query.options(db.joinedload(Order.order_items)).all()

    order_list = []
    for order in orders:
        order_data = {
            "order_id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "user_name": User.query.get(order.user_id).username,  # Fetch user name
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": []
        }

        for item in order.order_items:
            order_data["items"].append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase
            })

        order_list.append(order_data)

    return jsonify(order_list), 200


# Get Orders by User ID (Admin-only)" API
@order_bp.route("/admin/orders/<int:user_id>", methods=["GET"])
@jwt_required()
def get_orders_by_user(user_id):
    """Fetch all orders for a specific user (Admin-only)"""
    admin_id = get_jwt_identity()  # Get admin's ID from JWT

    # Fetch admin user
    admin_user = User.query.get(admin_id)
    if not admin_user or admin_user.role != "admin":
        return jsonify({"error": "Unauthorized, admin access only"}), 403

    # Fetch orders for the given user ID
    orders = Order.query.filter_by(user_id=user_id).all()

    if not orders:
        return jsonify({"message": "No orders found for this user"}), 404

    order_list = []
    for order in orders:
        order_data = {
            "order_id": order.id,
            "user_id": order.user_id,
            "username": User.query.get(order.user_id).username,  # Fetch username
            "total_price": order.total_price,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": []
        }

        for item in order.order_items:
            order_data["items"].append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase
            })

        order_list.append(order_data)

    return jsonify(order_list), 200
