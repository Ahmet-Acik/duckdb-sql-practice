# Database Configuration
# This file contains database connection settings
# Copy this file to config.py and update the values as needed

# DuckDB Database Path
DATABASE_PATH = 'hr_database.duckdb'

# Alternative: In-memory database (data will be lost when connection closes)
# DATABASE_PATH = ':memory:'

# Database Settings
DATABASE_CONFIG = {
    'path': DATABASE_PATH,
    'read_only': False,
    'config': {
        'memory_limit': '2GB',
        'threads': 4
    }
}