from flask import Blueprint, request, jsonify
import os
from app import db
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import OrderItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.activity_log import log_activity
from werkzeug.utils import secure_filename

product_bp = Blueprint("product", __name__)

# Configure upload folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'product_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_product_image(file, product_id):
    """Helper function to save a product image and return its URL"""
    if not file or not allowed_file(file.filename):
        return None

    # Create folder for product images if it doesn't exist
    product_folder = os.path.join(UPLOAD_FOLDER, f'product_{product_id}')
    os.makedirs(product_folder, exist_ok=True)

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(product_folder, filename)
    file.save(file_path)

    # Return the relative URL path for the database
    return f'/static/product_images/product_{product_id}/{filename}'


# Create Product
@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product = Product(name=data["name"], price=data["price"], stock=data["stock"], category_id=data["category_id"], )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201


# Add a new route for creating products with image
@product_bp.route("/products/with-image", methods=["POST"])
@jwt_required()
def add_product_with_image():
    """Create a new product with image upload support"""
    # Check if the request is a form with a file
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Get form data
    name = request.form.get('name')
    price = float(request.form.get('price', 0))
    stock = int(request.form.get('stock', 0))
    category_id = int(request.form.get('category_id', 0))

    if not name:
        return jsonify({"error": "Product name is required"}), 400

    # Create product first to get the ID
    product = Product(
        name=name,
        price=price,
        stock=stock,
        category_id=category_id
    )
    db.session.add(product)
    db.session.commit()

    # Now handle the image
    file = request.files['image']
    if file and file.filename:
        image_url = save_product_image(file, product.id)
        if image_url:
            product.image_url = image_url
            db.session.commit()

    # Log activity
    user_id = get_jwt_identity()
    log_activity(user_id, "Added Product", f"Added product: {name}")

    return jsonify({
        "message": "Product added successfully",
        "product": product.to_dict()
    }), 201


# Get All Products
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify([])  # Return an empty JSON list instead of None
    return jsonify([product.to_dict() for product in products])


# Get Single Product
@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


# Update Product
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    """Update product details (Admins Only)"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # 🔐 Check if user is an admin
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # 🔍 Find the product
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # ✅ Update fields if present in request
    if "name" in data:
        product.name = data["name"]
    if "price" in data and data["price"] >= 0:
        product.price = float(data["price"])
    if "stock" in data:
        if data["stock"] < 0:
            return jsonify({"error": "Stock cannot be negative"}), 400
        product.stock = int(data["stock"])
    if "category_id" in data:
        product.category_id = data["category_id"]
    if "image_url" in data:
        product.image_url = data["image_url"]

    db.session.commit()
    # Log the product update
    log_activity(user_id, "Updated Product", f"Updated product: {product.name}")
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200


# Add a separate route for updating products with image
@product_bp.route("/products/<int:product_id>/with-image", methods=["PUT"])
@jwt_required()
def update_product_with_image(product_id):
    """Update product with image upload support"""
    user_id = get_jwt_identity()

    # Check if user is an admin
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Find the product
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Update fields if present in form data
    if 'name' in request.form:
        product.name = request.form.get('name')
    if 'price' in request.form:
        price = float(request.form.get('price'))
        if price >= 0:
            product.price = price
    if 'stock' in request.form:
        stock = int(request.form.get('stock'))
        if stock >= 0:
            product.stock = stock
    if 'category_id' in request.form:
        product.category_id = int(request.form.get('category_id'))

    # Handle image upload
    if 'image' in request.files and request.files['image'].filename:
        image_url = save_product_image(request.files['image'], product_id)
        if image_url:
            product.image_url = image_url

    db.session.commit()
    # Log the product update
    log_activity(user_id, "Updated Product", f"Updated product: {product.name}")

    return jsonify({
        "message": "Product updated successfully",
        "product": product.to_dict()
    }), 200


# Image upload endpoint
@product_bp.route("/products/<int:product_id>/upload-image", methods=["POST"])
@jwt_required()
def upload_product_image(product_id):
    """Upload an image for an existing product"""
    user_id = get_jwt_identity()

    # Check if user is an admin
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Find the product
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check if the image file is in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the image
    image_url = save_product_image(file, product_id)
    if not image_url:
        return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400

    # Update the product with the new image URL
    product.image_url = image_url
    db.session.commit()

    # Log the activity
    log_activity(user_id, "Updated Product", f"Updated image for product: {product.name}")

    return jsonify({
        "message": "Product image uploaded successfully",
        "image_url": image_url,
        "product": product.to_dict()
    }), 200


# Delete a specific Product using ID
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200


# Sales of Products Endpoint
@product_bp.route("/products/sales", methods=["GET"])
@jwt_required()
def get_product_sales():
    products = Product.query.all()
    sales_data = []

    for product in products:
        total_sold = db.session.query(db.func.sum(OrderItem.quantity)).filter(
            OrderItem.product_id == product.id).scalar() or 0
        sales_data.append({
            "product_id": product.id,
            "name": product.name,
            "total_sold": total_sold
        })

    return jsonify(sales_data)


# Low Stock Notification Endpoint
@product_bp.route("/products/low-stock", methods=["GET"])
@jwt_required()
def get_low_stock_products():
    """Fetch products that are running low on stock"""
    threshold = request.args.get("threshold", 5, type=int)  # Default threshold = 5
    low_stock_products = Product.query.filter(Product.stock < threshold).all()

    return jsonify([product.to_dict() for product in low_stock_products]), 200


# Bulk Product Attribute Updates Endpoint
@product_bp.route("/products/bulk-update", methods=["PUT"])
@jwt_required()
def bulk_update_products():
    """Allow admin to update multiple products in a single request."""
    user_id = get_jwt_identity()  # Get logged-in user
    user = User.query.get(user_id)

    # Ensure only Admin can perform bulk updates
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if not isinstance(data, list):  # Ensure it's a list of products
        return jsonify({"error": "Invalid request format"}), 400

    updated_products = []
    errors = []

    for product_data in data:
        product_id = product_data.get("id")
        product = Product.query.get(product_id)

        if not product:
            errors.append({"product_id": product_id, "error": "Product not found"})
            continue

        # Update fields only if provided
        if "name" in product_data:
            product.name = product_data["name"]
        if "price" in product_data:
            product.price = float(product_data["price"])
        if "stock" in product_data:
            product.stock = int(product_data["stock"])
        if "category_id" in product_data:
            product.category_id = int(product_data["category_id"])
        if "image_url" in product_data:
            product.image_url = product_data["image_url"]

        updated_products.append(product)

    db.session.commit()

    return jsonify({
        "message": "Bulk product update successful",
        "updated_products": [product.to_dict() for product in updated_products],
        "errors": errors
    }), 200