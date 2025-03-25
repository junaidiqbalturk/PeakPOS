from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product


class SalesReport:
    @staticmethod
    def get_sales_summary(start_date=None, end_date=None):
        """Generate a sales summary within a date range"""
        query = db.session.query(
            func.sum(Order.total_price).label("total_revenue"),
            func.count(Order.id).label("total_orders")
        )

        if start_date and end_date:
            query = query.filter(Order.created_at.between(start_date, end_date))

        result = query.first()
        return {
            "total_revenue": result.total_revenue or 0,
            "total_orders": result.total_orders or 0,
            "start_date": start_date.strftime("%Y-%m-%d") if start_date else "All Time",
            "end_date": end_date.strftime("%Y-%m-%d") if end_date else "All Time"
        }

    @staticmethod
    def get_best_selling_products(limit=5):
        """Retrieve the top-selling products"""
        best_sellers = (
            db.session.query(
                Product.name,
                func.sum(OrderItem.quantity).label("total_sold")
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .group_by(Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )

        return [{"product": row.name, "total_sold": row.total_sold} for row in best_sellers]
