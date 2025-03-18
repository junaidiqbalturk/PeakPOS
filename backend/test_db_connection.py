from app import create_app, db
from sqlalchemy import text  # Import text function

# Create Flask app instance
app = create_app()

# Use application context
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))  # Use text() for raw SQL
        print("✅ Connected to MS SQL Successfully!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("greamesmith").encode('utf-8')
print("Hashed Password:", hashed_password)