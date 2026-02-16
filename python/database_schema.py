"""
Database schema for Portfolio Projects
Creates SQLite database with tables for all three projects
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"


def create_forecast_tables(conn):
    """Create tables for Forecast Accuracy project"""
    cursor = conn.cursor()

    # Products dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_cost REAL NOT NULL
        )
    """)

    # Regions dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regions (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    # Forecast data fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            product_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            forecast_quantity INTEGER NOT NULL,
            actual_quantity INTEGER NOT NULL,
            forecast_error INTEGER NOT NULL,
            absolute_error INTEGER NOT NULL,
            accuracy_pct REAL NOT NULL,
            forecast_method TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
        )
    """)

    # Create indexes for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_forecast_date
        ON forecast_data(date)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_forecast_product
        ON forecast_data(product_id)
    """)

    print("[+] Forecast Accuracy tables created")


def create_sales_tables(conn):
    """Create tables for Sales vs Budget project"""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL,
            business_unit TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            category_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            sales_amount REAL NOT NULL,
            budget_amount REAL NOT NULL,
            variance_amount REAL NOT NULL,
            variance_pct REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES sales_categories(category_id),
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sales_date
        ON sales_data(date)
    """)

    print("[+] Sales vs Budget tables created")


def create_inventory_tables(conn):
    """Create tables for Inventory Optimization project"""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            product_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            stock_level INTEGER NOT NULL,
            safety_stock INTEGER NOT NULL,
            abc_class TEXT NOT NULL CHECK(abc_class IN ('A', 'B', 'C')),
            xyz_class TEXT NOT NULL CHECK(xyz_class IN ('X', 'Y', 'Z')),
            holding_cost_daily REAL NOT NULL,
            demand_variance REAL NOT NULL,
            service_level_pct REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_inventory_date
        ON inventory_data(date)
    """)

    print("[+] Inventory Optimization tables created")


def initialize_database():
    """Initialize the complete database schema"""

    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    try:
        print(f"[*] Creating database at: {DB_PATH}")

        # Create all tables
        create_forecast_tables(conn)
        create_sales_tables(conn)
        create_inventory_tables(conn)

        # Commit changes
        conn.commit()
        print(f"\n[+] Database initialized successfully!")
        print(f"[*] Location: {DB_PATH}")

    except Exception as e:
        print(f"[-] Error creating database: {e}")
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
