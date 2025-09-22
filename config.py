# Database Configuration
# This file contains database connection settings

# DuckDB Database Path
DATABASE_PATH = 'hr_database.duckdb'

# Database Settings
DATABASE_CONFIG = {
    'read_only': False,
    'config': {
        'memory_limit': '2GB',
        'threads': 4
    }
}