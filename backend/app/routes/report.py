from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required
from sqlalchemy import func, desc, cast, Date
from datetime import datetime, timedelta
from app.models.order import Order, OrderItem
from app.models.product import Product

report_bp = Blueprint("report", __name__)


@report_bp.route("/sales-summary", methods=["GET"])
@jwt_required()
def sales_summary():
    try:
        # Get date range from query parameters
        try:
            start_date = request.args.get("start_date", (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
            end_date = request.args.get("end_date", datetime.now().strftime("%Y-%m-%d"))

            # Convert to datetime objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59)  # End of day
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Get summary metrics
        summary = db.session.query(
            func.sum(Order.total_price).label("total_revenue"),
            func.count(Order.id).label("total_orders")
        ).filter(
            Order.created_at.between(start_date, end_date)
        ).first()

        total_revenue = float(summary.total_revenue or 0)
        total_orders = int(summary.total_orders or 0)

        # MSSQL compatible date query
        daily_data_query = db.session.query(
            cast(Order.created_at, Date).label("date"),
            func.sum(Order.total_price).label("revenue"),
            func.count(Order.id).label("orders")
        ).filter(
            Order.created_at.between(start_date, end_date)
        ).group_by(
            cast(Order.created_at, Date)
        ).order_by(
            cast(Order.created_at, Date)
        ).all()

        # Format results
        daily_data = []
        for day in daily_data_query:
            daily_data.append({
                "date": str(day.date),
                "revenue": float(day.revenue or 0),
                "orders": int(day.orders or 0)
            })

        return jsonify({
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "daily_data": daily_data
        }), 200

    except Exception as e:
        print(f"Error in sales summary: {str(e)}")
        return jsonify({"error": "Failed to generate sales summary"}), 500


@report_bp.route("/best-selling-products", methods=["GET"])
@jwt_required()
def best_selling_products():
    try:
        # Get parameters
        limit = min(int(request.args.get("limit", 5)), 100)  # Cap at 100 for performance

        # Ultra simplified query - ONLY focusing on order items
        query = db.session.query(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.price_at_purchase * OrderItem.quantity).label("total_revenue")
        ).group_by(
            OrderItem.product_id
        ).order_by(
            desc("total_sold")
        ).limit(limit)

        result = query.all()

        # Separately fetch product details to avoid complex joins
        products_data = []
        for item in result:
            product = Product.query.get(item.product_id)
            if product:
                # Handle category that may be an object rather than a string
                category_name = None
                if hasattr(product, 'category'):
                    if isinstance(product.category, str):
                        category_name = product.category
                    elif hasattr(product.category, 'name'):
                        # If category is an object with a name attribute
                        category_name = product.category.name
                    else:
                        # Fallback: Get any identifiable property or just the id
                        category_name = str(product.category)

                products_data.append({
                    "id": product.id,
                    "name": product.name,
                    "category": category_name,
                    "total_sold": int(item.total_sold or 0),
                    "total_revenue": float(item.total_revenue or 0)
                })

        return jsonify(products_data), 200

    except Exception as e:
        print(f"Error in best selling products: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve best-selling products"
        }), 500


@report_bp.route("/inventory-status", methods=["GET"])
@jwt_required()
def inventory_status():
    try:
        # Query for low stock products
        low_stock_threshold = int(request.args.get("threshold", 10))

        low_stock = db.session.query(
            Product
        ).filter(
            Product.stock <= low_stock_threshold
        ).order_by(
            Product.stock
        ).limit(10).all()

        # Format the results - Handle Category objects
        low_stock_products = []
        for product in low_stock:
            # Handle category that may be an object rather than a string
            category_name = None
            if hasattr(product, 'category'):
                if isinstance(product.category, str):
                    category_name = product.category
                elif hasattr(product.category, 'name'):
                    # If category is an object with a name attribute
                    category_name = product.category.name
                else:
                    # Fallback: Convert to string representation
                    category_name = str(product.category)

            low_stock_products.append({
                "id": product.id,
                "name": product.name,
                "category": category_name,
                "quantity": product.stock,
                "price": float(product.price)
            })

        # Get overall inventory stats
        inventory_stats = db.session.query(
            func.count(Product.id).label("total_products"),
            func.sum(Product.stock).label("total_stock"),
            func.avg(Product.price).label("avg_price")
        ).first()

        return jsonify({
            "low_stock_products": low_stock_products,
            "inventory_stats": {
                "total_products": int(inventory_stats.total_products or 0),
                "total_stock": int(inventory_stats.total_stock or 0),
                "avg_price": float(inventory_stats.avg_price or 0),
                "low_stock_count": len(low_stock_products)
            }
        }), 200

    except Exception as e:
        print(f"Error in inventory status: {str(e)}")
        return jsonify({"error": "Failed to retrieve inventory status"}), 500