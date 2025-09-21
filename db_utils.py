"""
Database Connection Utilities for DuckDB HR Practice
This module provides connection utilities and helper functions.
"""

import duckdb
import pandas as pd
from pathlib import Path
from config import DATABASE_PATH, DATABASE_CONFIG

def get_connection():
    """
    Get a DuckDB connection using the configured settings.
    
    Returns:
        duckdb.DuckDBPyConnection: Database connection
    """
    return duckdb.connect(
        database=DATABASE_PATH,
        read_only=DATABASE_CONFIG.get('read_only', False),
        config=DATABASE_CONFIG.get('config', {})
    )

def execute_query(query, params=None):
    """
    Execute a SQL query and return results.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
        
    Returns:
        list: Query results
    """
    with get_connection() as conn:
        if params:
            result = conn.execute(query, params).fetchall()
        else:
            result = conn.execute(query).fetchall()
        return result

def query_to_dataframe(query, params=None):
    """
    Execute a SQL query and return results as a pandas DataFrame.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
        
    Returns:
        pd.DataFrame: Query results as DataFrame
    """
    with get_connection() as conn:
        if params:
            df = conn.execute(query, params).df()
        else:
            df = conn.execute(query).df()
        return df

def show_tables():
    """Show all tables in the database."""
    query = "SHOW TABLES"
    return execute_query(query)

def describe_table(table_name):
    """
    Describe the structure of a table.
    
    Args:
        table_name (str): Name of the table to describe
        
    Returns:
        list: Table structure information
    """
    query = f"DESCRIBE {table_name}"
    return execute_query(query)

def table_info():
    """Get information about all tables and their record counts."""
    tables = ['regions', 'countries', 'locations', 'departments', 'jobs', 'employees', 'dependents']
    info = {}
    
    with get_connection() as conn:
        for table in tables:
            count_row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            count = count_row[0] if count_row is not None else 0
            columns = conn.execute(f"DESCRIBE {table}").fetchall()
            info[table] = {
                'count': count,
                'columns': [col[0] for col in columns]
            }
    
    return info

def print_query_results(query, title=None, limit=10):
    """
    Execute a query and print results in a formatted way.
    
    Args:
        query (str): SQL query to execute
        title (str, optional): Title to display above results
        limit (int): Maximum number of rows to display
    """
    if title:
        print(f"\n{title}")
        print("=" * len(title))
    
    df = query_to_dataframe(query)
    if len(df) > limit:
        print(f"Showing first {limit} of {len(df)} rows:")
        print(df.head(limit).to_string(index=False))
        print(f"... ({len(df) - limit} more rows)")
    else:
        print(df.to_string(index=False))
    print()

if __name__ == "__main__":
    # Test the connection and show database info
    print("Database Connection Test")
    print("=" * 30)
    
    # Show tables
    tables = show_tables()
    print("Available tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Show table information
    print("\nTable Information:")
    info = table_info()
    for table_name, table_data in info.items():
        print(f"\n{table_name.upper()}:")
        print(f"  Records: {table_data['count']}")
        print(f"  Columns: {', '.join(table_data['columns'])}")