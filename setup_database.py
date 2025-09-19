"""
Database Setup Script for DuckDB HR Practice
This script creates the HR database schema and loads sample data into DuckDB.
"""

import duckdb
import os
from pathlib import Path

def setup_database(db_path='hr_database.duckdb'):
    """
    Set up the HR database with schema and data.
    
    Args:
        db_path: Path to the DuckDB database file
    """
    # Get the project root directory
    project_root = Path(__file__).parent
    schema_file = project_root / 'data' / 'schema.sql'
    data_file = project_root / 'data' / 'data.sql'
    
    # Connect to DuckDB
    conn = duckdb.connect(db_path)
    
    try:
        print("Setting up HR database...")
        
        # Read and execute schema
        print("Creating tables...")
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        conn.execute(schema_sql)
        print("✓ Tables created successfully")
        
        # Read and execute data
        print("Loading data...")
        with open(data_file, 'r') as f:
            data_sql = f.read()
        conn.execute(data_sql)
        print("✓ Data loaded successfully")
        
        # Verify the setup by counting records in each table
        tables = ['regions', 'countries', 'locations', 'departments', 'jobs', 'employees', 'dependents']
        print("\nDatabase setup complete! Record counts:")
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {count} records")
            
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
    print("\nHR database is ready for practice!")