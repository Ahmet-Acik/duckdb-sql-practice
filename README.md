# DuckDB SQL Practice

A comprehensive collection of SQL practice exercises using DuckDB and Python, featuring real-world HR database scenarios.

## 🎯 Learning Objectives

This project provides hands-on practice with:
- **SQL Fundamentals**: SELECT, WHERE, JOIN, GROUP BY, ORDER BY
- **Advanced SQL**: Subqueries, CTEs, Window Functions, Set Operations
- **DuckDB Features**: High-performance analytical SQL database
- **Python Integration**: Using DuckDB with Python for data analysis
- **Real-world Scenarios**: HR database with realistic relationships

## 🗄️ Database Schema

The practice database contains 7 interconnected tables:

```
regions (4 records)
├── countries (25 records)
    ├── locations (7 records)
        ├── departments (11 records)
            ├── employees (40 records)
                ├── dependents (30 records)
jobs (19 records)
    ├── employees (references job_id)
```

### Entity Relationships
- **Regions** → Countries → Locations → Departments → Employees
- **Jobs** → Employees (many-to-one)
- **Employees** → Dependents (one-to-many)
- **Employees** → Employees (manager hierarchy)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Setup
1. **Clone or download the project**
   ```bash
   cd /path/to/duckdb-sql-practice
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python setup_database.py
   ```

   This creates `hr_database.duckdb` with all tables and sample data.

## 📚 Practice Modules

### Core SQL Topics

| Module | File | Topics Covered |
|--------|------|----------------|
| **01** | `01_intro_select.py` | Basic SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, CASE |
| **02** | `02_joins.py` | INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF joins |
| **03** | `03_aggregation.py` | COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING, Window functions |
| **04** | `04_subqueries_ctes.py` | Scalar, correlated subqueries, CTEs, recursive CTEs |

### Advanced Topics (Coming Soon)
- **05** Set Operations (UNION, INTERSECT, EXCEPT)
- **06** Data Modification (INSERT, UPDATE, DELETE)
- **07** Advanced Analytics (PIVOT, time series, statistical functions)
- **08** Performance Optimization (indexing, query plans)

## 🛠️ Usage

### Running Individual Modules
```bash
# Basic SELECT operations
python 01_intro_select.py

# JOIN operations
python 02_joins.py

# Aggregation and GROUP BY
python 03_aggregation.py

# Subqueries and CTEs
python 04_subqueries_ctes.py
```

### Using the Database Utilities
```python
from db_utils import get_connection, print_query_results, query_to_dataframe

# Execute a custom query
print_query_results(
    "SELECT * FROM employees WHERE salary > 10000",
    "High Earners"
)

# Get results as pandas DataFrame
df = query_to_dataframe("SELECT * FROM departments")
print(df.head())
```

### Interactive Exploration
```python
from db_utils import table_info

# Get overview of all tables
info = table_info()
for table, data in info.items():
    print(f"{table}: {data['count']} records")
```

## 🔧 Configuration

Database configuration is managed in `config.py`:

```python
# Database path
DATABASE_PATH = 'hr_database.duckdb'

# DuckDB settings
DATABASE_CONFIG = {
    'read_only': False,
    'config': {
        'memory_limit': '2GB',
        'threads': 4
    }
}
```

To use a different database location or settings:
1. Copy `config_template.py` to `config.py`
2. Modify the settings as needed
3. Re-run `setup_database.py`

## 📊 Sample Queries

### Basic Analysis
```sql
-- Employee count by department
SELECT d.department_name, COUNT(e.employee_id) as employee_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
ORDER BY employee_count DESC;
```

### Advanced Analysis with CTE
```sql
WITH salary_stats AS (
    SELECT 
        department_id,
        AVG(salary) as avg_salary,
        COUNT(*) as emp_count
    FROM employees
    GROUP BY department_id
)
SELECT 
    d.department_name,
    ss.emp_count,
    ROUND(ss.avg_salary, 2) as avg_salary
FROM departments d
JOIN salary_stats ss ON d.department_id = ss.department_id
WHERE ss.emp_count >= 3
ORDER BY ss.avg_salary DESC;
```

## 🎯 Practice Exercises

Each module includes:
- **Commented examples** explaining the concepts
- **Progressive difficulty** from basic to advanced
- **Real-world scenarios** based on HR analytics
- **Performance tips** and best practices

### Suggested Learning Path
1. Start with `01_intro_select.py` for SQL basics
2. Master joins with `02_joins.py`
3. Learn aggregation in `03_aggregation.py`
4. Advance to subqueries with `04_subqueries_ctes.py`
5. Experiment with your own queries using the utilities

## 📁 Project Structure

```
duckdb-sql-practice/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── setup_database.py          # Database creation script
├── config.py                  # Database configuration
├── config_template.py         # Configuration template
├── db_utils.py                # Database utilities
├── .gitignore                 # Git ignore rules
├── data/                      # SQL files
│   ├── schema.sql            # Table definitions
│   └── data.sql              # Sample data
├── 01_intro_select.py        # SELECT basics
├── 02_joins.py               # JOIN operations
├── 03_aggregation.py         # Aggregation functions
├── 04_subqueries_ctes.py     # Subqueries and CTEs
└── hr_database.duckdb        # Generated database file
```

## 🔍 Database Schema Details

### Tables and Relationships

**employees** (40 records)
- Primary key: `employee_id`
- Foreign keys: `job_id` → jobs, `department_id` → departments, `manager_id` → employees
- Contains: name, email, phone, hire_date, salary

**departments** (11 records)
- Primary key: `department_id`
- Foreign key: `location_id` → locations
- Contains: department_name

**jobs** (19 records)
- Primary key: `job_id`
- Contains: job_title, min_salary, max_salary

**locations** (7 records)
- Primary key: `location_id`
- Foreign key: `country_id` → countries
- Contains: street_address, postal_code, city, state_province

**countries** (25 records)
- Primary key: `country_id`
- Foreign key: `region_id` → regions
- Contains: country_name

**regions** (4 records)
- Primary key: `region_id`
- Contains: region_name (Europe, Americas, Asia, Middle East and Africa)

**dependents** (30 records)
- Primary key: `dependent_id`
- Foreign key: `employee_id` → employees
- Contains: first_name, last_name, relationship

## 🚀 DuckDB Features Demonstrated

- **Analytical Functions**: Window functions, percentiles, statistical aggregates
- **SQL Compatibility**: Standard SQL with PostgreSQL extensions
- **Performance**: Fast analytical queries on structured data
- **Python Integration**: Seamless pandas DataFrame integration
- **Data Types**: Rich type system including dates, JSON, arrays
- **CTEs and Subqueries**: Advanced query composition patterns

## 🤝 Contributing

Feel free to:
- Add new practice modules
- Improve existing examples
- Fix bugs or enhance documentation
- Share interesting queries you've created

## 📖 Additional Resources

- [DuckDB Documentation](https://duckdb.org/docs/)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [DuckDB Python API](https://duckdb.org/docs/api/python/overview)
- [Advanced SQL Concepts](https://mode.com/sql-tutorial/)

## 🐛 Troubleshooting

### Common Issues

**Database file not found**
- Run `python setup_database.py` to create the database

**Import errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Permission errors**
- Check file permissions in the project directory
- Ensure `.venv` directory is writable

**Query errors**
- Check SQL syntax in your custom queries
- Refer to DuckDB documentation for supported features

---

**Happy Learning!** 🎉 Start with the basic modules and work your way up to advanced SQL patterns. Each script includes detailed examples and explanations to guide your learning journey.
3. Import your HR schema/data (see `data/` and scripts for details)

## Project Structure
- `data/` — Place for CSV, Parquet, or SQLite files
- `scripts/` — Modular Python scripts for each SQL topic (to be created)
- `README.md` — This file
- `.gitignore`, `requirements.txt` — Standard Python project files

## Next Steps
- Add scripts to load schema/data into DuckDB
- Implement modular SQL topic scripts
- Document usage and best practices
