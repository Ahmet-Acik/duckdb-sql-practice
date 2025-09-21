"""
Database Setup Script for DuckDB HR Practice
This script creates the HR database schema and loads sample data into DuckDB.
"""

import duckdb
import os
from pathlib import Path
from config import DATABASE_PATH, DATABASE_CONFIG

def setup_database(db_path=None):
    """
    Set up the HR database with schema and data.
    
    Args:
        db_path: Path to the DuckDB database file (uses config if not provided)
    """
    if db_path is None:
        db_path = DATABASE_PATH
    
    # Get the project root directory
    project_root = Path(__file__).parent
    schema_file = project_root / 'data' / 'schema.sql'
    data_file = project_root / 'data' / 'data.sql'
    
    # Connect to DuckDB with configuration
    conn = duckdb.connect(
        database=db_path,
        read_only=DATABASE_CONFIG.get('read_only', False),
        config=DATABASE_CONFIG.get('config', {})
    )
    
    try:
        print(f"Setting up HR database at: {db_path}")
        
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
            result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            count = result[0] if result is not None else 0
            print(f"  {table}: {count} records")
            
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
    print("\nHR database is ready for practice!")