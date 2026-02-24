# How to Manage Data for Forecast Accuracy Dashboard

This guide explains how to replace the mock data with your own data and customize the plots in the [forecast-accuracy.html](pages/forecast-accuracy.html) dashboard.

---

## 📋 Table of Contents

1. [Understanding the Data Pipeline](#understanding-the-data-pipeline)
2. [Option 1: Using Your Own CSV Data](#option-1-using-your-own-csv-data)
3. [Option 2: Modifying the Python Data Generator](#option-2-modifying-the-python-data-generator)
4. [Option 3: Direct JSON Editing](#option-3-direct-json-editing)
5. [Data Structure Reference](#data-structure-reference)
6. [Customizing Charts](#customizing-charts)
7. [Troubleshooting](#troubleshooting)

---

## 🔄 Understanding the Data Pipeline

The dashboard uses a three-step data pipeline:

```
Step 1: Create Database
├─ python/database_schema.py
└─ Creates: data/portfolio.db (SQLite database)

Step 2: Populate Database
├─ python/generate_data.py
└─ Populates database with forecast data

Step 3: Export to JSON
├─ python/export_to_json.py
└─ Creates: data/json/forecast-accuracy.json

Step 4: Visualize
├─ pages/forecast-accuracy.html
└─ Reads JSON and renders charts
```

---

## 🎯 Option 1: Using Your Own CSV Data

**Best for:** Importing data from Excel or CSV files

### Step 1: Prepare Your CSV File

Create a CSV file with the following columns:

```csv
date,product_name,category,region_name,forecast_quantity,actual_quantity,forecast_method
2023-01-01,Product A,Category 1,North America,1000,950,Enhanced Time Series
2023-01-01,Product B,Category 2,Europe,1500,1600,Legacy Moving Average
```

**Required columns:**
- `date` - Format: YYYY-MM-DD
- `product_name` - Name of the product
- `category` - Product category (e.g., Hoses, Belts, Timing Systems)
- `region_name` - Geographic region
- `forecast_quantity` - Forecasted quantity
- `actual_quantity` - Actual quantity sold/used
- `forecast_method` - Method used (e.g., "Enhanced Time Series", "Legacy Moving Average")

### Step 2: Create Import Script

Create a new file `python/import_csv.py`:

```python
"""
Import forecast data from CSV file
"""
import sqlite3
import csv
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
CSV_PATH = Path(__file__).parent.parent / "data" / "your_data.csv"  # UPDATE THIS

def import_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM forecast_data")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM regions")

    # Track unique products and regions
    products = {}
    regions = {}
    product_id = 1
    region_id = 1

    # Read CSV and prepare data
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Add product if new
            product_key = (row['product_name'], row['category'])
            if product_key not in products:
                products[product_key] = product_id
                cursor.execute(
                    "INSERT INTO products VALUES (?, ?, ?, ?)",
                    (product_id, row['product_name'], row['category'], 0.0)
                )
                product_id += 1

            # Add region if new
            region_name = row['region_name']
            if region_name not in regions:
                regions[region_name] = region_id
                cursor.execute(
                    "INSERT INTO regions VALUES (?, ?, ?)",
                    (region_id, region_name, '')
                )
                region_id += 1

            # Calculate metrics
            forecast_qty = int(row['forecast_quantity'])
            actual_qty = int(row['actual_quantity'])
            forecast_error = forecast_qty - actual_qty
            absolute_error = abs(forecast_error)
            accuracy_pct = (1 - (absolute_error / actual_qty)) * 100 if actual_qty > 0 else 0

            # Insert forecast record
            cursor.execute("""
                INSERT INTO forecast_data
                (date, product_id, region_id, forecast_quantity, actual_quantity,
                 forecast_error, absolute_error, accuracy_pct, forecast_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['date'],
                products[product_key],
                regions[region_name],
                forecast_qty,
                actual_qty,
                forecast_error,
                absolute_error,
                round(accuracy_pct, 2),
                row['forecast_method']
            ))

    conn.commit()
    conn.close()
    print(f"✅ Import complete! {len(products)} products, {len(regions)} regions")

if __name__ == "__main__":
    import_csv_to_db()
```

### Step 3: Run the Pipeline

```bash
# 1. Create database schema
python python/database_schema.py

# 2. Import your CSV data
python python/import_csv.py

# 3. Export to JSON
python python/export_to_json.py
```

### Step 4: Refresh the Dashboard

Open [pages/forecast-accuracy.html](pages/forecast-accuracy.html) in your browser - it will automatically load your data!

---

## 🔧 Option 2: Modifying the Python Data Generator

**Best for:** Customizing the mock data generation

Edit [python/generate_data.py](python/generate_data.py):

### Customize Products

```python
# Line 25-34: Modify products list
products = [
    (1, "Your Product 1", "Your Category 1", 12.50),
    (2, "Your Product 2", "Your Category 2", 18.75),
    # Add more products...
]
```

### Customize Regions

```python
# Line 42-49: Modify regions list
regions = [
    (1, "Your Region 1", "Country 1"),
    (2, "Your Region 2", "Country 2"),
    # Add more regions...
]
```

### Adjust Date Range

```python
# Line 60: Modify date range
generate_forecast_data(conn, start_date="2024-01-01", end_date="2026-12-31")
```

### Customize Accuracy Improvement

```python
# Line 95: Adjust improvement factor
# Current: starts at 80% accuracy, improves to 96%
improvement_factor = 0.80 + (0.16 * (month_count / total_months))

# Your custom range (e.g., 70% to 95%):
improvement_factor = 0.70 + (0.25 * (month_count / total_months))
```

Then run the pipeline:

```bash
python python/database_schema.py
python python/generate_data.py  # Uses your modified code
python python/export_to_json.py
```

---

## ✍️ Option 3: Direct JSON Editing

**Best for:** Quick testing or small datasets

Directly edit [data/json/forecast-accuracy.json](data/json/forecast-accuracy.json):

### JSON Structure

```json
{
  "metadata": {
    "title": "Your Title",
    "total_records": 1000
  },
  "kpis": {
    "overall_accuracy": 92.5,
    "improvement_pct": 23.0,
    "total_forecasts": 1000,
    "avg_absolute_error": 150,
    "best_accuracy": 98.5
  },
  "charts": {
    "monthly_trend": {
      "labels": ["2023-01", "2023-02", ...],
      "data": [85.2, 86.5, ...]
    },
    "category_performance": {
      "labels": ["Category 1", "Category 2", ...],
      "data": [92.0, 88.5, ...]
    },
    "region_performance": {
      "labels": ["Region 1", "Region 2", ...],
      "data": [90.0, 93.0, ...]
    },
    "method_comparison": {
      "labels": ["Method 1", "Method 2"],
      "data": [85.0, 95.0]
    },
    "error_distribution": {
      "labels": [70, 75, 80, 85, 90, 95, 100],
      "data": [5, 15, 45, 120, 200, 150, 50]
    }
  }
}
```

---

## 📊 Data Structure Reference

### Database Tables

**products**
| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Unique product ID |
| product_name | TEXT | Product name |
| category | TEXT | Product category |
| unit_cost | REAL | Cost per unit |

**regions**
| Column | Type | Description |
|--------|------|-------------|
| region_id | INTEGER | Unique region ID |
| region_name | TEXT | Region name |
| country | TEXT | Primary country |

**forecast_data**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment ID |
| date | DATE | Forecast date (YYYY-MM-DD) |
| product_id | INTEGER | Foreign key to products |
| region_id | INTEGER | Foreign key to regions |
| forecast_quantity | INTEGER | Forecasted quantity |
| actual_quantity | INTEGER | Actual quantity |
| forecast_error | INTEGER | forecast - actual |
| absolute_error | INTEGER | abs(error) |
| accuracy_pct | REAL | 100 × (1 - abs_error/actual) |
| forecast_method | TEXT | Method used |

---

## 🎨 Customizing Charts

Edit [pages/forecast-accuracy.html](pages/forecast-accuracy.html):

### Change Chart Colors

```javascript
// Line 359: Trend chart color
borderColor: '#667eea',  // Change to your color
backgroundColor: 'rgba(102, 126, 234, 0.1)',

// Line 402-409: Category chart colors
backgroundColor: [
  '#667eea',  // Color 1
  '#764ba2',  // Color 2
  '#f093fb',  // Color 3
  // Add more colors...
]
```

### Adjust Chart Scale

```javascript
// Line 380-387: Y-axis range for trend chart
scales: {
  y: {
    beginAtZero: false,
    min: 70,    // Change minimum
    max: 100,   // Change maximum
  }
}
```

### Change Chart Type

```javascript
// Line 395: Change bar to line
type: 'bar',  // Options: 'bar', 'line', 'pie', 'doughnut', 'radar'
```

### Modify Chart Titles and Descriptions

```html
<!-- Line 244-247: Main chart title -->
<h3 class="chart-title">📈 Your Custom Title</h3>
<p class="chart-description">
  Your custom description text
</p>
```

### Add New Charts

Add a new chart container in the HTML:

```html
<!-- Add after line 305 -->
<div class="chart-container">
  <div class="chart-header">
    <h3 class="chart-title">🆕 My New Chart</h3>
    <p class="chart-description">Description</p>
  </div>
  <div class="chart-wrapper">
    <canvas id="myNewChart"></canvas>
  </div>
</div>
```

Add the chart creation function:

```javascript
// Add in JavaScript section (after line 538)
function createMyNewChart() {
  const ctx = document.getElementById('myNewChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.charts.your_data.labels,
      datasets: [{
        label: 'My Data',
        data: chartData.charts.your_data.data,
        backgroundColor: '#667eea'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

// Call it in loadData() function (around line 334)
createMyNewChart();
```

---

## 🔍 Troubleshooting

### Issue: "Error loading data"

**Solution:**
1. Check that `data/json/forecast-accuracy.json` exists
2. Verify JSON is valid (use [JSONLint](https://jsonlint.com/))
3. Run the data pipeline again:
   ```bash
   python python/database_schema.py
   python python/generate_data.py
   python python/export_to_json.py
   ```

### Issue: Charts are empty

**Solution:**
1. Open browser console (F12)
2. Look for JavaScript errors
3. Verify data structure matches expected format
4. Check that chart data arrays are not empty

### Issue: Wrong data displayed

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check JSON file modification date
4. Re-export JSON: `python python/export_to_json.py`

### Issue: KPIs show "--"

**Solution:**
- KPIs load from `chartData.kpis` object
- Verify JSON has correct structure:
  ```json
  "kpis": {
    "overall_accuracy": 92.5,
    "improvement_pct": 23.0,
    ...
  }
  ```

### Issue: Import fails with encoding errors

**Solution:**
- Save CSV with UTF-8 encoding
- In Excel: Save As → CSV UTF-8
- Add encoding parameter: `open(file, encoding='utf-8-sig')`

---

## 🚀 Quick Start Checklist

- [ ] Prepare your data in CSV format (see Option 1)
- [ ] Create database: `python python/database_schema.py`
- [ ] Import data: `python python/import_csv.py` (or use generate_data.py)
- [ ] Export to JSON: `python python/export_to_json.py`
- [ ] Open `pages/forecast-accuracy.html` in browser
- [ ] Verify all charts display correctly
- [ ] Customize colors/labels as needed
- [ ] Test with different data to ensure robustness

---

## 📚 Additional Resources

- **Chart.js Documentation**: https://www.chartjs.org/docs/
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Python CSV Module**: https://docs.python.org/3/library/csv.html

---

## 💡 Tips

1. **Start Small**: Test with a small dataset first (100-200 records)
2. **Validate Data**: Ensure dates are consistent and metrics are calculated correctly
3. **Backup**: Keep a copy of original data before modifications
4. **Version Control**: Commit changes after successful data updates
5. **Performance**: For large datasets (>10,000 records), consider data aggregation in SQL

---

**Last Updated**: February 16, 2026
**Author**: Enrico Stancanelli
**Project**: Portfolio - Forecast Accuracy Dashboard
