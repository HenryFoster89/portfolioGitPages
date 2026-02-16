# Portfolio Data Pipeline

Python scripts for generating, managing, and exporting portfolio project data.

## 🏗️ Architecture Overview

```
SQLite Database (portfolio.db)
         ↓
    Python Scripts
         ↓
   JSON Files (data/json/)
         ↓
  HTML + Chart.js (Interactive Web Charts)
```

## 📁 File Structure

```
python/
├── database_schema.py     # Create database tables
├── generate_data.py       # Generate realistic mock data
├── export_to_json.py      # Export SQLite → JSON for charts
├── requirements.txt       # Python dependencies
└── README.md             # This file

data/
├── portfolio.db          # SQLite database (auto-generated)
└── json/                 # Exported JSON files
    └── forecast-accuracy.json
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Create Database Schema

```bash
python database_schema.py
```

**Output:**
```
📊 Creating database at: data/portfolio.db
✅ Forecast Accuracy tables created
✅ Sales vs Budget tables created
✅ Inventory Optimization tables created
✅ Database initialized successfully!
```

### Step 3: Generate Mock Data

```bash
python generate_data.py
```

**Output:**
```
🚀 Starting data generation...
✅ Dimension data inserted
📊 Generating 36 months of forecast data...
✅ Generated 1,728 forecast records

📈 Data Summary:
   Total Records: 1,728
   Average Accuracy: 87.45%
   Min Accuracy: 45.23%
   Max Accuracy: 99.87%
```

### Step 4: Export to JSON

```bash
python export_to_json.py
```

**Output:**
```
🚀 Starting JSON export...
✅ Exported forecast accuracy data to data/json/forecast-accuracy.json
   📊 1,728 total records
   🎯 87.45% overall accuracy
   📈 23.0% improvement
✅ JSON export completed successfully!
```

### Step 5: View in Browser

1. Open `pages/forecast-accuracy.html` in your browser
2. Or use a local server:
   ```bash
   python -m http.server 8000
   # Then visit: http://localhost:8000/pages/forecast-accuracy.html
   ```

## 📊 Database Schema

### Forecast Accuracy Tables

**products** - Product dimension
- `product_id` (PK)
- `product_name`
- `category`
- `unit_cost`

**regions** - Region dimension
- `region_id` (PK)
- `region_name`
- `country`

**forecast_data** - Main fact table
- `id` (PK)
- `date` - Month of forecast
- `product_id` (FK)
- `region_id` (FK)
- `forecast_quantity` - Predicted demand
- `actual_quantity` - Actual demand
- `forecast_error` - Difference (forecast - actual)
- `absolute_error` - Absolute difference
- `accuracy_pct` - Accuracy percentage
- `forecast_method` - Method used (Legacy/Enhanced)

### Sales vs Budget Tables (Future)
- `sales_categories`
- `sales_data`

### Inventory Tables (Future)
- `inventory_data`

## 🎯 Generated Data Characteristics

### Forecast Accuracy
- **Time Period:** 3 years (2023-01 to 2025-12)
- **Records:** ~1,700+ forecasts
- **Products:** 8 products across 4 categories
- **Regions:** 6 regions (EMEA, APAC, Americas)
- **Patterns:**
  - Seasonal variation (Q4 peak, Q3 dip)
  - Gradual accuracy improvement over time (80% → 95%)
  - Method transition mid-period (Legacy → Enhanced)
  - Realistic forecast errors with normal distribution

### Key Metrics Generated
- ✅ 23% accuracy improvement
- ✅ Average accuracy: ~87%
- ✅ Realistic seasonal patterns
- ✅ Product/region variations

## 📈 JSON Export Format

**forecast-accuracy.json structure:**

```json
{
  "metadata": {
    "title": "Forecast Accuracy Analysis",
    "generated": "2026-02-16T...",
    "total_records": 1728
  },
  "kpis": {
    "overall_accuracy": 87.45,
    "improvement_pct": 23.0,
    "total_forecasts": 1728,
    "avg_absolute_error": 142
  },
  "charts": {
    "monthly_trend": { /* Time series data */ },
    "category_performance": { /* Category breakdown */ },
    "region_performance": { /* Region breakdown */ },
    "method_comparison": { /* Before/after comparison */ },
    "error_distribution": { /* Histogram data */ }
  },
  "filters": {
    "products": [...],
    "categories": [...],
    "regions": [...]
  }
}
```

## 🔧 Customization

### Modify Data Generation

**Change date range:**
```python
# In generate_data.py
generate_forecast_data(conn, start_date="2022-01-01", end_date="2026-12-31")
```

**Add more products:**
```python
# In generate_data.py, function insert_dimension_data()
products = [
    (9, "New Product", "New Category", 50.00),
    # ... add more
]
```

**Adjust accuracy improvement:**
```python
# In generate_data.py, function generate_forecast_data()
improvement_factor = 0.75 + (0.20 * (month_count / total_months))
# ^ Change 0.75 (start) and 0.20 (improvement range)
```

### Modify Chart Queries

Edit `export_to_json.py` to change what data is exported:

```python
# Example: Add weekly instead of monthly aggregation
cursor.execute("""
    SELECT
        strftime('%Y-%W', date) as week,
        AVG(accuracy_pct) as avg_accuracy
    FROM forecast_data
    GROUP BY week
""")
```

## 🔄 Complete Workflow

```bash
# Full refresh (database → JSON → view)
python database_schema.py && \
python generate_data.py && \
python export_to_json.py

# Then open pages/forecast-accuracy.html
```

## 🎨 Chart Types Available

The HTML page includes:
1. **Line Chart** - Accuracy trend over time
2. **Bar Chart** - Category performance
3. **Doughnut Chart** - Region distribution
4. **Horizontal Bar** - Method comparison
5. **Histogram** - Error distribution

Built with **Chart.js 4.4** - fully interactive with hover tooltips, legends, and responsive design.

## 🚧 Next Steps

To add the other two projects:

1. **Sales vs Budget:**
   ```bash
   # Uncomment/implement generate_sales_data() in generate_data.py
   # Create export_sales() in export_to_json.py
   # Create pages/sales-vs-budget.html
   ```

2. **Inventory Optimization:**
   ```bash
   # Implement generate_inventory_data() in generate_data.py
   # Create export_inventory() in export_to_json.py
   # Create pages/inventory-analysis.html
   ```

## 📝 Notes

- **SQLite database** is committed to git (small size, ~2MB)
- **JSON files** are also committed (optimized for web delivery)
- **No server required** - all static files work on GitHub Pages
- **Data is mock** - replace with real data by modifying generate_data.py

## 🐛 Troubleshooting

**Error: Database not found**
```bash
# Run schema creation first
python database_schema.py
```

**Error: No JSON file**
```bash
# Run the complete pipeline
python generate_data.py && python export_to_json.py
```

**Charts not loading**
- Check browser console for errors
- Ensure JSON path is correct: `../data/json/forecast-accuracy.json`
- Use a local web server (not file:// protocol)

## 📚 Resources

- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [SQLite Python Tutorial](https://docs.python.org/3/library/sqlite3.html)
- [NumPy Random](https://numpy.org/doc/stable/reference/random/index.html)
