# duckdb-sql-practice

A comprehensive Python + DuckDB project for learning and practicing SQL analytics, DML, and procedural logic. Includes modular scripts for each SQL topic, sample HR data, and best practices for data science and analytics workflows.

## Features
- Modular scripts for: SELECT, JOIN, set operators, aggregation, subqueries, CTEs, pivoting, DML, transactions, procedural logic, error handling
- Sample HR schema and data (import from SQLite or CSV/Parquet)
- Clean Python project structure with virtual environment support
- Best practices for reproducible analytics

## Setup

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
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
