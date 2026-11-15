# Import db correctly
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize db here

# Import models after db is initialized
from app.models.tenant import Tenant, TenantBranch
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order, OrderItem
from app.models.discount import Discount
from app.models.supplier import Supplier
from app.models.receipt import Receipt
from app.models.receipt_settings import ReceiptSettings
