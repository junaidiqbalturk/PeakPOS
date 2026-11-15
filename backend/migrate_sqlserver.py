import sys
sys.path.insert(0, 'backend')
from app import create_app, db

app = create_app()
with app.app_context():
    print('Target Database URI:', db.engine.url)

    sql_statements = [
        """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tenants' AND xtype='U')
        CREATE TABLE tenants (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(120) NOT NULL,
            slug NVARCHAR(80) NOT NULL UNIQUE,
            business_type NVARCHAR(50) DEFAULT 'retail',
            currency NVARCHAR(10) DEFAULT 'USD',
            tax_rate FLOAT DEFAULT 7.0,
            [plan] NVARCHAR(30) DEFAULT 'starter',
            status NVARCHAR(20) DEFAULT 'active',
            created_at DATETIME DEFAULT GETUTCDATE()
        );
        """,
        """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tenant_branches' AND xtype='U')
        CREATE TABLE tenant_branches (
            id INT IDENTITY(1,1) PRIMARY KEY,
            tenant_id INT NOT NULL,
            name NVARCHAR(100) NOT NULL,
            code NVARCHAR(30) NOT NULL,
            address NVARCHAR(255) NULL,
            is_main BIT DEFAULT 0,
            created_at DATETIME DEFAULT GETUTCDATE()
        );
        """,
        "IF COL_LENGTH('[user]', 'tenant_id') IS NULL ALTER TABLE [user] ADD tenant_id INT NULL;",
        "IF COL_LENGTH('[user]', 'pin_code') IS NULL ALTER TABLE [user] ADD pin_code NVARCHAR(10) NULL;",
        "IF COL_LENGTH('[user]', 'is_active') IS NULL ALTER TABLE [user] ADD is_active BIT DEFAULT 1;",
        "IF COL_LENGTH('product', 'tenant_id') IS NULL ALTER TABLE product ADD tenant_id INT NULL;",
        "IF COL_LENGTH('product', 'barcode') IS NULL ALTER TABLE product ADD barcode NVARCHAR(100) NULL;",
        "IF COL_LENGTH('product', 'cost_price') IS NULL ALTER TABLE product ADD cost_price FLOAT DEFAULT 0.0;",
        "IF COL_LENGTH('category', 'tenant_id') IS NULL ALTER TABLE category ADD tenant_id INT NULL;",
        "IF COL_LENGTH('[order]', 'tenant_id') IS NULL ALTER TABLE [order] ADD tenant_id INT NULL;",
        "IF COL_LENGTH('discount', 'tenant_id') IS NULL ALTER TABLE discount ADD tenant_id INT NULL;",
        "IF COL_LENGTH('receipt_settings', 'tenant_id') IS NULL ALTER TABLE receipt_settings ADD tenant_id INT NULL;"
    ]

    for sql in sql_statements:
        try:
            db.session.execute(db.text(sql))
            db.session.commit()
            print("Executed:", sql.strip().splitlines()[0])
        except Exception as e:
            print("Error executing:", e)
            db.session.rollback()

    # Ensure default tenant exists
    row = db.session.execute(db.text("SELECT id FROM tenants WHERE slug='default-store'")).fetchone()
    if not row:
        insert_sql = """
        INSERT INTO tenants (name, slug, business_type, currency, tax_rate, [plan], status)
        VALUES ('PeakPOS Flagship Store', 'default-store', 'retail', 'USD', 7.0, 'enterprise', 'active');
        """
        db.session.execute(db.text(insert_sql))
        db.session.commit()
        row = db.session.execute(db.text("SELECT id FROM tenants WHERE slug='default-store'")).fetchone()
        print("Created default tenant #", row[0])
    else:
        print("Default tenant exists #", row[0])

    default_tenant_id = row[0]
    db.session.execute(db.text(f"UPDATE [user] SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.execute(db.text(f"UPDATE product SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.execute(db.text(f"UPDATE category SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.execute(db.text(f"UPDATE [order] SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.execute(db.text(f"UPDATE discount SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.execute(db.text(f"UPDATE receipt_settings SET tenant_id = {default_tenant_id} WHERE tenant_id IS NULL"))
    db.session.commit()

    # Check or create test cashier in SQL Server if not present
    cashier = db.session.execute(db.text("SELECT id FROM [user] WHERE email='cashier@peakpos.com'")).fetchone()
    if not cashier:
        from flask_bcrypt import generate_password_hash
        pwd = generate_password_hash("123456").decode('utf-8')
        db.session.execute(db.text(f"""
        INSERT INTO [user] (username, email, password_hash, role, tenant_id, is_active)
        VALUES ('cashier_test', 'cashier@peakpos.com', '{pwd}', 'cashier', {default_tenant_id}, 1)
        """))
        db.session.commit()
        print("Created cashier@peakpos.com in SQL Server")
    else:
        print("cashier@peakpos.com exists in SQL Server")

    print("\n✅ SQL Server Migration and Backfill complete!")
