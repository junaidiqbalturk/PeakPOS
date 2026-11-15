import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app import create_app, db

app = create_app()

with app.app_context():
    # 1. Add currency_symbol to tenants table if not exists
    sql = """
    IF NOT EXISTS (
        SELECT * FROM sys.columns 
        WHERE object_id = OBJECT_ID('tenants') AND name = 'currency_symbol'
    )
    BEGIN
        ALTER TABLE tenants ADD currency_symbol NVARCHAR(10) DEFAULT '$';
        PRINT 'Added currency_symbol column to tenants table';
    END
    ELSE
    BEGIN
        PRINT 'currency_symbol column already exists in tenants';
    END
    """
    db.session.execute(db.text(sql))
    db.session.commit()

    # Update default tenant to have currency_symbol
    db.session.execute(db.text("UPDATE tenants SET currency_symbol = '$' WHERE currency_symbol IS NULL"))
    db.session.commit()
    print("Database migration for currency_symbol completed successfully.")
