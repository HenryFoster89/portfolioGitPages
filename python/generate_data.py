"""
Generate realistic mock data for Portfolio Projects
Focuses on Forecast Accuracy Analysis with realistic patterns
"""

import sqlite3
import random
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)


def insert_dimension_data(conn):
    """Insert reference data for products and regions"""
    cursor = conn.cursor()

    # Products data
    products = [
        (1, "Automotive Hose A", "Hoses", 12.50),
        (2, "Automotive Hose B", "Hoses", 18.75),
        (3, "Belt Assembly X", "Belts", 24.00),
        (4, "Belt Assembly Y", "Belts", 32.50),
        (5, "Timing System Z", "Timing Systems", 45.00),
        (6, "Cooling Component C", "Cooling", 28.00),
        (7, "Accessory Drive D", "Accessories", 15.50),
        (8, "Industrial Belt E", "Industrial", 38.00),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)",
        products
    )

    # Regions data
    regions = [
        (1, "EMEA North", "Germany"),
        (2, "EMEA South", "Italy"),
        (3, "APAC East", "China"),
        (4, "APAC South", "India"),
        (5, "Americas North", "USA"),
        (6, "Americas South", "Brazil"),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO regions VALUES (?, ?, ?)",
        regions
    )

    conn.commit()
    print("[+] Dimension data inserted")


def generate_forecast_data(conn, start_date="2023-01-01", end_date="2025-12-31"):
    """
    Generate realistic forecast accuracy data with:
    - Seasonal patterns
    - Product-specific bias
    - Gradual improvement over time (23% improvement)
    - Regional variations
    """
    cursor = conn.cursor()

    # Get products and regions
    cursor.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT region_id FROM regions")
    region_ids = [row[0] for row in cursor.fetchall()]

    # Date range
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate monthly data
    current_date = start
    forecast_records = []

    month_count = 0
    total_months = ((end.year - start.year) * 12 + end.month - start.month)

    print(f"[*] Generating {total_months} months of forecast data...")

    while current_date <= end:
        month_count += 1

        # Improvement factor: starts at 0.80 accuracy, improves to 0.95+
        # This represents the 23% improvement mentioned in portfolio
        improvement_factor = 0.80 + (0.16 * (month_count / total_months))

        for product_id in product_ids:
            for region_id in region_ids:

                # Base demand with seasonality
                base_demand = random.randint(800, 1500)

                # Seasonal factor (higher in Q4, lower in Q3)
                month = current_date.month
                if month in [10, 11, 12]:  # Q4 peak
                    seasonal_factor = 1.3
                elif month in [7, 8, 9]:   # Q3 dip
                    seasonal_factor = 0.8
                else:
                    seasonal_factor = 1.0

                actual_quantity = int(base_demand * seasonal_factor)

                # Forecast with improving accuracy over time
                # Early forecasts have more error, later ones are better
                error_std = 250 * (1 - improvement_factor)  # Decreasing error over time

                forecast_error = int(np.random.normal(0, error_std))
                forecast_quantity = actual_quantity + forecast_error

                # Ensure non-negative
                forecast_quantity = max(50, forecast_quantity)

                # Calculate metrics
                absolute_error = abs(forecast_quantity - actual_quantity)
                accuracy_pct = (1 - (absolute_error / actual_quantity)) * 100 if actual_quantity > 0 else 0
                accuracy_pct = max(0, min(100, accuracy_pct))  # Clamp to 0-100

                # Forecast method (improved method introduced mid-way)
                if month_count < total_months / 2:
                    forecast_method = "Legacy Moving Average"
                else:
                    forecast_method = "Enhanced Time Series"

                forecast_records.append((
                    current_date.strftime("%Y-%m-%d"),
                    product_id,
                    region_id,
                    forecast_quantity,
                    actual_quantity,
                    forecast_error,
                    absolute_error,
                    round(accuracy_pct, 2),
                    forecast_method
                ))

        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    # Insert all records
    cursor.executemany("""
        INSERT INTO forecast_data
        (date, product_id, region_id, forecast_quantity, actual_quantity,
         forecast_error, absolute_error, accuracy_pct, forecast_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, forecast_records)

    conn.commit()
    print(f"[+] Generated {len(forecast_records)} forecast records")

    # Print summary statistics
    cursor.execute("""
        SELECT
            COUNT(*) as total_records,
            ROUND(AVG(accuracy_pct), 2) as avg_accuracy,
            ROUND(MIN(accuracy_pct), 2) as min_accuracy,
            ROUND(MAX(accuracy_pct), 2) as max_accuracy
        FROM forecast_data
    """)

    stats = cursor.fetchone()
    print(f"\n[*] Data Summary:")
    print(f"   Total Records: {stats[0]:,}")
    print(f"   Average Accuracy: {stats[1]}%")
    print(f"   Min Accuracy: {stats[2]}%")
    print(f"   Max Accuracy: {stats[3]}%")


def main():
    """Main data generation process"""

    print("[*] Starting data generation...\n")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    try:
        # Insert dimension data
        insert_dimension_data(conn)

        # Generate forecast accuracy data
        generate_forecast_data(conn)

        print("\n[+] All data generated successfully!")

    except Exception as e:
        print(f"[-] Error generating data: {e}")
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
